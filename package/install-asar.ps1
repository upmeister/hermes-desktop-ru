param([switch]$Doctor)

$ErrorActionPreference = 'Stop'
# install-asar.ps1 v6 (hybrid) - install ALL Hermes Desktop mods (ru-mod + timestamps).
# NOTE: pure ASCII (PS 5.1 reads .ps1 without BOM as ANSI; UTF-8 bytes -> ParserError).
# RULE v2 (13.08.2026): NEVER ship a package dist as the install base - it wipes
# other mods. Install base = fresh `npm run build` from the clone. Package dist is
# fallback only.
# v3 (13.08): restores the mod into the clone BEFORE building - patches are git-applied
#   if not present, untracked locale files are copied from files/ (updates wipe them too).
# v4 (15.08): desktop-timestamps-mod.patch REMOVED - upstream 0.20.4 ships native
#   timestamps via display.timestamps.
# v5 (16.08): structural-i18n.mjs registers 'ru' by anchors (types/catalog/languages).
# v6 HYBRID (20.08): git-патч остаётся источником правок. Три защитных слоя:
#   (1) git restore --source=HEAD --staged --worktree . ПЕРЕД apply -
#       чинит root-причину «патч слетает после апдейта»: клон уже модифицирован
#       прошлыми волнами -> git apply --check даёт конфликт -> молча пропускает
#       весь патч (обжиг 20.08: PLATFORM_TAGLINES не лёг). restore возвращает
#       tracked к стоку, untracked-локали НЕ трогает.
#   (2) version-gate: файл EXPECTED_COMMIT рядом со скриптом (SHA апстрима, на
#       котором собран мод); расхождение -> WARNING (не блокирует, но честно
#       предупреждает о риске несовпадения хунков).
#   (3) doctor: `-Doctor` режим - сухой прогон `git apply --check --3way` на
#       РЕАЛЬНОМ состоянии клона + отчёт по числу файлов патча; используется
#       и перед билдом (если check не проходит - останавливаемся с понятной
#       причиной, НЕ замалчивая как v5).

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

Write-Host "== Hermes Desktop mod install (v6 hybrid: restore + gate + build + asar rebuild) =="
if (-not (Test-Path $asarJs)) { Write-Host "FAIL: asar.js not found (clone missing?)"; exit 1 }

Get-Process -Name Hermes -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# ---------- version-gate: сравнение коммита апстрима в клоне с ожидаемым ----------
$actualCommit = ""
Push-Location $root
$actualCommit = (& cmd /c "git rev-parse HEAD 2>nul")
Pop-Location
if (-not $actualCommit) { $actualCommit = "(git недоступен?!)" }
if (Test-Path $expectFile) {
  $expectedCommit = (Get-Content $expectFile -Raw).Trim()
  Write-Host ("version-gate: clone HEAD=" + $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length)))
  Write-Host ("              expected = " + $expectedCommit.Substring(0, [Math]::Min(12, $expectedCommit.Length)))
  if ("$actualCommit".Trim() -ne $expectedCommit -and -not ($actualCommit.StartsWith($expectedCommit) -or $expectedCommit.StartsWith("$actualCommit".Trim().Substring(0, [Math]::Min(7, $actualCommit.Length))))) {
    Write-Host "WARN: апстрим в клоне НЕ совпадает с версией, на которой собран мод."
    Write-Host "      Патч может не лечь чисто после апдейта. Продолжаем (restore+apply+doctor проверят),"
    Write-Host "      но при конфликтах хунков придётся обновлять мод под новый апстрим."
  } else {
    Write-Host "OK: клон на ожидаемом коммите."
  }
} else {
  Write-Host ("version-gate: EXPECTED_COMMIT не найден, пропуск сравнения (HEAD=" + $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length)) + ")")
}

# ---------- 0. RESTORE клона к стоку (tracked; untracked-локали выживают) ----------
Push-Location $root
cmd /c "git restore --source=HEAD --staged --worktree . 2>nul"
$restoreExit = $LASTEXITCODE
Pop-Location
Write-Host ("restore к стоку: exit=" + $restoreExit + " (untracked-локали не тронуты)")

# ---------- doctor: сухой прогон apply (по реальному состоянию клона) ----------
$doctorAnyFail = $false
foreach ($p in @("ru-mod-v3.patch")) {
  $patch = Join-Path $PSScriptRoot "patches\$p"
  if (-not (Test-Path $patch)) { Write-Host ("doctor: патч не найден: " + $p); continue }
  Push-Location $root
  cmd /c "git apply --check --3way $patch 2>nul"
  $chk = $LASTEXITCODE
  Pop-Location
  if ($chk -eq 0) {
    Write-Host ("doctor: apply check OK  ($p)")
  } else {
    Write-Host ("doctor: apply check FAIL ($p) -> хунки не лягут на этот сток")
    $doctorAnyFail = $true
  }
}
if ($Doctor) {
  # Отдельный доктор-режим: отчёт о состоянии и выход
  Write-Host ""
  Write-Host "=== DOCTOR REPORT ==="
  Write-Host ("клон HEAD       : " + $actualCommit)
  Write-Host ("restore exit    : " + $restoreExit)
  Write-Host ("patch check     : " + $(if ($doctorAnyFail) {"FAIL - конфликт с апстримом"} else {"OK"}))
  Push-Location $root
  $dirty = (& cmd /c "git status --short 2>nul")
  Pop-Location
  Write-Host ("tracked dirty   : " + ($(if ($dirty) {$dirty} else {"(чисто)"})))
  Write-Host "Рекомендации:"
  Write-Host "  - если doctor FAIL: апстрим ушёл вперёд -> обновить мод (rebase патча / вариант C в перспективе)"
  Write-Host "  - если только dirty: клон тронут -> restore в начале install уже это чинит"
  exit $(if ($doctorAnyFail) {1} else {0})
}
if ($doctorAnyFail) {
  Write-Host "FAIL: сухая проверка патча показала конфликт с состоянием клона. Останавливаемся до ручного разбора."
  Write-Host "  - проверь: git status в клоне (может, untracked-локали кто-то правил), свежий апстрим?"
  exit 1
}

# ---------- 0b. ПРИМЕНЕНИЕ патча (теперь на чистом стоке) ----------
Push-Location $root
foreach ($p in @("ru-mod-v3.patch")) {
  $patch = Join-Path $PSScriptRoot "patches\$p"
  if (Test-Path $patch) {
    cmd /c "git apply --check --3way $patch 2>nul"
    if ($LASTEXITCODE -eq 0) {
      cmd /c "git apply --3way $patch 2>nul"
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
if ((Test-Path $asar) -and -not (Test-Path "$asar.stock.bak")) { Copy-Item $asar "$asar.stock.bak" }
if ((Test-Path "$unpacked\dist") -and -not (Test-Path "$unpacked\dist.stock.bak")) { Copy-Item "$unpacked\dist" "$unpacked\dist.stock.bak" -Recurse }
Write-Host "backups ok"

# 1b. structural i18n patcher (registers 'ru' in types/catalog/languages by anchors)
$i18nDir = "$root\apps\desktop\src\i18n"
if (Test-Path "$PSScriptRoot\structural-i18n.mjs") {
  node "$PSScriptRoot\structural-i18n.mjs" "$i18nDir"
  if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: structural-i18n patcher"; exit 1 }
  Write-Host "structural-i18n done"
} else {
  Write-Host "WARN: structural-i18n.mjs missing - falling back to patch hunks (may already be applied)"
}

# 2. BUILD dist from the clone
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

# 3. unpack-marked files
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

# 7. wipe unpacked; pack: everything unpacked-marked
if (Test-Path $unpacked) { Remove-Item $unpacked -Recurse -Force }
node $asarJs pack $app $asar --unpack "**" | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: pack"; exit 1 }

# 8. checks
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
