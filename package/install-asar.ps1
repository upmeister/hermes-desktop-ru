$ErrorActionPreference = 'Stop'
# install-asar.ps1 v2 - install ALL clone mods into packaged Hermes Desktop.
# NOTE: pure ASCII (PS 5.1 reads .ps1 without BOM as ANSI; UTF-8 bytes -> quotes -> ParserError).
# RULE (13.08.2026): NEVER ship a package dist as the install base - it wipes other
# clone mods (ru-mod got wiped by v1). The install base is ALWAYS the freshly built
# clone dist: step 1 = npm run build in apps\desktop (includes ALL patches living in
# the clone), step 2 = asar rebuild with that dist. Package dist/ is fallback only.
$root = "C:\Users\covhnw\AppData\Local\hermes\hermes-agent"
$desktop = "$root\apps\desktop"
$res = "$desktop\release\win-unpacked\resources"
$asar = "$res\app.asar"
$asarJs = "$root\node_modules\@electron\asar\bin\asar.js"
$modDist = Join-Path $PSScriptRoot "dist"
$tmp = Join-Path $env:TEMP ("asar-mod-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$app = "$tmp\app"
$unpacked = "$res\app.asar.unpacked"

Write-Host "== Hermes Desktop mod install (v2: clone build + asar rebuild) =="
if (-not (Test-Path $asarJs)) { Write-Host "FAIL: asar.js not found (clone missing?)"; exit 1 }

Get-Process -Name Hermes -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

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
$chunkName = "none"
if (Test-Path "$unpacked\dist\assets") {
  $ru = node -e "const fs=require('fs');for(const f of fs.readdirSync('$unpacked\dist\assets').filter(f=>f.endsWith('.js'))){const s=fs.readFileSync('$unpacked\dist\assets\'+f,'utf8');if(s.includes('\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c')){console.log(f);break}}"
  if ($ru) { $ruMarker = "FOUND ($ru)"; $chunkName = $ru }
}
Write-Host ("checks: index=" + $physIndex + " main=" + $physMain + " pkg=" + $physPkg + " ru=" + $ruMarker)
if (-not ($physIndex -and $physMain -and $physPkg)) { Write-Host "WARN: checks failed - restore from .stock.bak"; exit 1 }

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "INSTALL OK - restart Hermes Desktop (ru marker proves clone build)"
