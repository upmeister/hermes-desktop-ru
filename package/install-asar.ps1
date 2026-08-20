param([switch]$Doctor)

$ErrorActionPreference = 'Stop'
# install-asar.ps1 v7 (variant C) - install ru-mod into Hermes Desktop.
# Replaces git apply --3way with the structural anchor registry engine:
#   apply-hardcodes.mjs <repoRoot> registry.json [--doctor]
#
# WHY (20.08.2026, three crashes root-caused):
#   git apply --3way on a SHALLOW clone returns EXIT 0 even when 3-way merge
#   leaves conflict markers (<<<<<<< ours / >>>>>>> theirs) in the files;
#   vite build then dies on "Encountered diff marker". Both our installer v6
#   and hermes-ru died EXACTLY that way (same files: presets.ts,
#   custom-endpoints-settings.tsx). The engine searches full unique line
#   blocks instead (survives upstream reflow), is idempotent, and reports
#   MISSING/AMBIGUOUS explicitly - a real doctor, no silent breakage.
#
# Steps: version-gate (EXPECTED_COMMIT, warn-only) -> restore tracked to HEAD
#        -> doctor (engine --doctor, FAIL aborts) -> apply (engine) ->
#        structural-i18n (register 'ru') -> copy untracked locale files ->
#        backup asar -> npm run build -> asar rebuild -> probe-ru.
#
# NOTE: pure ASCII on purpose (PS 5.1 reads .ps1 without BOM as ANSI).

$root = "C:\Users\covhnw\AppData\Local\hermes\hermes-agent"
$desktop = "$root\apps\desktop"
$res = "$desktop\release\win-unpacked\resources"
$asar = "$res\app.asar"
$asarJs = "$root\node_modules\@electron\asar\bin\asar.js"
$modDist = Join-Path $PSScriptRoot "dist"
$tmp = Join-Path $env:TEMP ("asar-mod-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$app = "$tmp\app"
$unpacked = "$res\app.asar.unpacked"
$expectFile = Join-Path $PSScriptRoot "EXPECTED_COMMIT"
$registry = Join-Path $PSScriptRoot "registry.json"

Write-Host "== Hermes Desktop mod install (v7 structural registry: restore + doctor + apply + build + asar) =="
if (-not (Test-Path $registry)) { Write-Host "FAIL: registry.json not found next to installer"; exit 1 }

# ---------- ensure deps: public-release installer fixes its own node_modules ----------
# Hermes updates can leave node_modules partial or with broken nodes (observed
# 20.08: vite present but @electron/asar + electron-builder missing; later an
# @tabler/icons-react node with dist/ but no package.json, which made vite fail
# to resolve it). deps-health.mjs requires the key packages; exit 1 => rebuild.
$healthBad = $false
node "$PSScriptRoot\deps-health.mjs" $root
if ($LASTEXITCODE -ne 0) { $healthBad = $true }
if ($healthBad) {
  if (Test-Path "$root\package-lock.json") {
    Write-Host "WARN: node_modules unhealthy - running 'npm ci' (clean rebuild from lockfile, 3-10 min)..."
    Push-Location $root
    cmd /c "npm ci 2>&1"
    Pop-Location
  } else {
    Write-Host "WARN: node_modules unhealthy, no package-lock.json - running 'npm install'..."
    Push-Location $root
    cmd /c "npm install 2>&1"
    Pop-Location
  }
  # re-check
  node "$PSScriptRoot\deps-health.mjs" $root
  if ($LASTEXITCODE -ne 0) {
    Write-Host "FAIL: node_modules still missing packages after rebuild - check npm network"; exit 1
  }
  Write-Host "node_modules rebuilt"
} else {
  Write-Host "deps: node_modules healthy"
}
if (-not (Test-Path $asarJs)) { Write-Host "FAIL: @electron/asar not found after deps step"; exit 1 }

Get-Process -Name Hermes -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# ---------- version-gate: compare clone HEAD vs the build the registry targets ----------
$actualCommit = ""
Push-Location $root
$actualCommit = (& cmd /c "git rev-parse HEAD 2>nul")
Pop-Location
if (-not $actualCommit) { $actualCommit = "(git unavailable?)" }
if (Test-Path $expectFile) {
  $expectedCommit = (Get-Content $expectFile -Raw).Trim()
  Write-Host ("version-gate: clone HEAD=" + $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length)))
  Write-Host ("              expected = " + $expectedCommit.Substring(0, [Math]::Min(12, $expectedCommit.Length)))
  if ("$actualCommit".Trim() -ne $expectedCommit -and -not ($actualCommit.StartsWith($expectedCommit) -or $expectedCommit.StartsWith("$actualCommit".Trim().Substring(0, [Math]::Min(7, $actualCommit.Length))))) {
    Write-Host "WARN: clone HEAD differs from the version the registry was generated for."
    Write-Host "      The engine doctor below is the real gate: if it passes 100%, the registry"
    Write-Host "      still fits this upstream. If it reports MISSING, re-run gen-registry.mjs"
    Write-Host "      on the new patch (or update overrides.json) before installing."
  } else {
    Write-Host "OK: clone is on the expected commit."
  }
} else {
  Write-Host ("version-gate: EXPECTED_COMMIT not found, skip (HEAD=" + $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length)) + ")")
}

# ---------- 0. RESTORE tracked files to HEAD (untracked locales survive) ----------
Push-Location $root
cmd /c "git restore --source=HEAD --staged --worktree . 2>nul"
$restoreExit = $LASTEXITCODE
Pop-Location
Write-Host ("restore to stock: exit=" + $restoreExit + " (untracked locale files untouched)")

# ---------- doctor: engine dry-run (WILL NOT WRITE) ----------
$doctorFail = $false
Push-Location $root
node "$PSScriptRoot\apply-hardcodes.mjs" $root $registry --doctor
$doctorExit = $LASTEXITCODE
Pop-Location
if ($doctorExit -ne 0) {
  Write-Host "FAIL: registry doctor reports MISSING/AMBIGUOUS rules."
  Write-Host "      The mod does NOT fit this upstream version without updating the registry."
  Write-Host "      Re-run gen-registry.mjs on a fresh patch, or fix overrides.json."
  if ($Doctor) {
    Write-Host ""
    Write-Host "=== DOCTOR REPORT ==="
    Write-Host ("clone HEAD : " + $actualCommit)
    Write-Host ("registry   : " + $registry)
    Write-Host "status: FAIL - engine found unapplicable rules"
    exit 1
  }
  exit 1
} else {
  Write-Host "doctor: registry applies 100%"
}
if ($Doctor) {
  Write-Host ""
  Write-Host "=== DOCTOR REPORT ==="
  Write-Host ("clone HEAD : " + $actualCommit)
  Write-Host ("registry   : " + $registry)
  Write-Host "status: OK - all rules apply cleanly (engine dry-run, nothing written)"
  exit 0
}

# ---------- 1. APPLY the registry (structural replacements, idempotent) ----------
Push-Location $root
node "$PSScriptRoot\apply-hardcodes.mjs" $root $registry
$applyExit = $LASTEXITCODE
Pop-Location
if ($applyExit -ne 0) { Write-Host "FAIL: registry apply aborted"; exit 1 }
Write-Host "apply: registry applied"

# ---------- 2. untracked locale/component files (always overwrite - part of the mod) ----------
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

# ---------- 3. backups (first run only) ----------
if ((Test-Path $asar) -and -not (Test-Path "$asar.stock.bak")) { Copy-Item $asar "$asar.stock.bak" }
if ((Test-Path "$unpacked\dist") -and -not (Test-Path "$unpacked\dist.stock.bak")) { Copy-Item "$unpacked\dist" "$unpacked\dist.stock.bak" -Recurse }
Write-Host "backups ok"

# ---------- 4. structural i18n patcher (register 'ru' in types/catalog/languages) ----------
$i18nDir = "$root\apps\desktop\src\i18n"
if (Test-Path "$PSScriptRoot\structural-i18n.mjs") {
  node "$PSScriptRoot\structural-i18n.mjs" "$i18nDir"
  if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: structural-i18n patcher"; exit 1 }
  Write-Host "structural-i18n done"
} else {
  Write-Host "WARN: structural-i18n.mjs missing - 'ru' registration may be missing from bundle"
}

# ---------- 5. BUILD dist from the clone ----------
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

# ---------- 6. asar rebuild (extract with stubs -> replace dist -> pack) ----------
$unpackedFiles = @()
foreach ($line in (node $asarJs list -i $asar)) {
  if ($line -match '^unpack\s*:\s*(.+)$') { $unpackedFiles += $Matches[1].Trim().TrimStart('\') }
}
Write-Host ("unpack-marked: " + $unpackedFiles.Count)

foreach ($f in $unpackedFiles) {
  $dest = Join-Path $unpacked ($f -replace '/', '\')
  $dir = Split-Path $dest -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  if (-not (Test-Path $dest)) { [System.IO.File]::WriteAllText($dest, '') }
}

New-Item -ItemType Directory -Path $app -Force | Out-Null
node $asarJs extract $asar $app | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: extract"; exit 1 }

if ($usePackage) { $srcDist = $modDist } else { $srcDist = "$desktop\dist" }
if (Test-Path "$app\dist") { Remove-Item "$app\dist" -Recurse -Force }
Copy-Item $srcDist "$app\dist" -Recurse
Write-Host ("dist from: " + $(if ($usePackage) { "package" } else { "clone build" }))

if (Test-Path $unpacked) { Remove-Item $unpacked -Recurse -Force }
node $asarJs pack $app $asar --unpack "**" | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: pack"; exit 1 }

# ---------- 7. checks ----------
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
