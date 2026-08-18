$ErrorActionPreference = 'Stop'
# install-asar.ps1 v3 - install ALL Hermes Desktop mods (ru-mod + timestamps).
# NOTE: pure ASCII (PS 5.1 reads .ps1 without BOM as ANSI; UTF-8 bytes -> ParserError).
# RULE v2 (13.08.2026): NEVER ship a package dist as the install base - it wipes
# other mods. Install base = fresh `npm run build` from the clone. Package dist is
# fallback only.
# v3 (13.08): (1) restores the mod into the clone BEFORE building - patches
# (ru-mod-v3) are git-applied if not present, untracked locale files are copied
# from files/ (updates wipe them too, not only tracked patches!);
# (2) RU marker probe moved to probe-ru.mjs (inline node -e breaks on backslash
# paths: \U -> SyntaxError).
# v4 (15.08, 0.20.4): desktop-timestamps-mod.patch REMOVED — upstream 0.20.4
# ships native timestamps gated by display.timestamps (config.yaml #41531);
# our mod timestamps were obsolete AND broke the build.
$root = "C:\Users\covhnw\AppData\Local\hermes\hermes-agent"
$desktop = "$root\apps\desktop"
$res = "$desktop\release\win-unpacked\resources"
$asar = "$res\app.asar"
$asarJs = "$root\node_modules\@electron\asar\bin\asar.js"
$modDist = Join-Path $PSScriptRoot "dist"
$tmp = Join-Path $env:TEMP ("asar-mod-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$app = "$tmp\app"
$unpacked = "$res\app.asar.unpacked"

Write-Host "== Hermes Desktop mod install (v3: restore + clone build + asar rebuild) =="
if (-not (Test-Path $asarJs)) { Write-Host "FAIL: asar.js not found (clone missing?)"; exit 1 }

Get-Process -Name Hermes -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# 0. RESTORE the mod into the clone (updates wipe tracked patches AND untracked files)
Push-Location $root
foreach ($p in @("ru-mod-v3.patch")) {
  $patch = Join-Path $PSScriptRoot "patches\$p"
  if (Test-Path $patch) {
    # PS 5.1: git writes progress to STDERR. With ErrorActionPreference=Stop, BOTH
    # `2>$null` and `2>&1 | Out-Null` AND `cmd /c "git ..."` still throw
    # NativeCommandError (stderr leaks through cmd). Verified fix (13.08): redirect
    # stderr INSIDE the cmd string (`2>nul`) - PS then sees no stderr at all.
    # $LASTEXITCODE still comes from git via cmd.
    cmd /c "git apply --check --3way $patch 2>nul" | Out-Null
    if ($LASTEXITCODE -eq 0) {
      cmd /c "git apply --3way $patch 2>nul" | Out-Null
      Write-Host "patch applied: $p"
    } else {
      Write-Host "patch skip (already applied or conflict): $p"
    }
  }
}
Pop-Location
# untracked locale/component files (always overwrite - they are part of the mod).
$files = @(
  @("files\ru.ts", "apps\desktop\src\i18n\ru.ts"),
  @("files\ru-constants.ts", "apps\desktop\src\app\settings\ru-constants.ts"),
  @("files\ru-locales.ts", "apps\desktop\src\plugins\kanban\ru-locales.ts")
)
foreach ($f in $files) {
  $src = Join-Path $PSScriptRoot $f[0]
  $dst = Join-Path $root $f[1]
  if (Test-Path $src) {
    $dir = Split-Path $dst -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Copy-Item $src $dst -Force
    Write-Host ("file restored: " + $f[1])
  }
}

# 1. backups (first run only)
# NOTE: parens around Test-Path REQUIRED before -and (PS parses -and as a parameter)
if ((Test-Path $asar) -and -not (Test-Path "$asar.stock.bak")) { Copy-Item $asar "$asar.stock.bak" }
if ((Test-Path "$unpacked\dist") -and -not (Test-Path "$unpacked\dist.stock.bak")) { Copy-Item "$unpacked\dist" "$unpacked\dist.stock.bak" -Recurse }
Write-Host "backups ok"

# 2. BUILD dist from the clone (includes ALL clone patches: timestamps + ru + ...)
Write-Host "building dist from clone (npm run build)..."
Push-Location $desktop
cmd /c "npm run build > $env:TEMP\mod-build.log 2>&1"
$buildExit = $LASTEXITCODE
Pop-Location
if ($buildExit -ne 0) {
  Write-Host "WARN: npm run build failed (exit $buildExit) - see $env:TEMP\mod-build.log"
  Write-Host "fallback: using package dist/ if present"
  if (Test-Path "$modDist\index.html") { Write-Host "using package dist fallback" }
  else { Write-Host "FAIL: no package dist either"; exit 1 }
  $usePackage = $true
} else {
  Write-Host "build OK"
  $usePackage = $false
}

# 3. unpack-marked files (format: "unpack : \path")
$unpackedFiles = @()
foreach ($line in (node $asarJs list -i $asar)) {
  if ($line -match '^unpack\s*:\s*(.+)$') { $unpackedFiles += $Matches[1].Trim().TrimStart('\') }
}
Write-Host ("unpack-marked: " + $unpackedFiles.Count)

# 4. stubs (empty) - asar extract requires marked files to exist physically
foreach ($f in $unpackedFiles) {
  $dest = Join-Path $unpacked ($f -replace '/', '\')
  $dir = Split-Path $dest -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  if (-not (Test-Path $dest)) { [System.IO.File]::WriteAllText($dest, '') }
}

# 5. extract
New-Item -ItemType Directory -Path $app -Force | Out-Null
node $asarJs extract $asar $app | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: extract"; exit 1 }

# 6. replace dist
if ($usePackage) { $srcDist = $modDist } else { $srcDist = "$desktop\dist" }
if (Test-Path "$app\dist") { Remove-Item "$app\dist" -Recurse -Force }
Copy-Item $srcDist "$app\dist" -Recurse
Write-Host ("dist from: " + $(if ($usePackage) { "package" } else { "clone build" }))

# 7. wipe unpacked; pack: everything unpacked-marked (only ONE --unpack honored;
#    "dist/**" does NOT match Windows backslash paths, "**" does)
if (Test-Path $unpacked) { Remove-Item $unpacked -Recurse -Force }
node $asarJs pack $app $asar --unpack "**" | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: pack"; exit 1 }

# 8. checks: physical files + RU marker in bundle (proves clone build had ru-mod)
$physIndex = Test-Path "$unpacked\dist\index.html"
$physMain = Test-Path "$unpacked\dist\electron-main.mjs"
$physPkg = Test-Path "$unpacked\package.json"
$ruMarker = "no"
if (Test-Path "$unpacked\dist\assets") {
  $ru = node "$PSScriptRoot\probe-ru.mjs" "$unpacked\dist\assets"
  if ($ru -and $ru -ne "NONE") { $ruMarker = "FOUND ($ru)" }
}
Write-Host ("checks: index=" + $physIndex + " main=" + $physMain + " pkg=" + $physPkg + " ru=" + $ruMarker)
if (-not ($physIndex -and $physMain -and $physPkg)) { Write-Host "WARN: checks failed - restore from .stock.bak"; exit 1 }
if ($ruMarker -eq "no") { Write-Host "WARN: RU marker not found - ru-mod may be missing from this build" }

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "INSTALL OK - restart Hermes Desktop to see the mods"
