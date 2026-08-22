param(
  [switch]$Doctor,
  [switch]$Help,
  [string]$Root
)

$ErrorActionPreference = 'Stop'
# install-asar.ps1 v1.0.1 (variant C)
# Structural anchor registry installer for hermes-desktop-ru.
# Pure logic in ASCII identifiers; user-facing messages may be Russian (UTF-8 BOM required).

function Show-Help {
  @"
Hermes Desktop RU - установщик мода

Использование:
  install.ps1                 Установить / переустановить мод
  install.ps1 -Doctor         Сухая проверка совместимости (ничего не пишет)
  install.ps1 -Root <path>    Явный путь к клону hermes-agent
  install.ps1 -Help           Эта справка

Также можно:
  install.bat                 То же через двойной клик (с паузой в конце)
  $env:HERMES_AGENT_ROOT      Переопределить путь к клону

Требования:
  - Hermes Desktop из исходников (git clone), не prebuilt .exe
  - Node.js 18+ и npm
  - Закрытый Hermes Desktop на время установки

По умолчанию ищет клон в:
  %LOCALAPPDATA%\hermes\hermes-agent
"@ | Write-Host
}

if ($Help) { Show-Help; exit 0 }

function Resolve-HermesRoot {
  param([string]$Explicit)
  $candidates = @()
  if ($Explicit) { $candidates += $Explicit }
  if ($env:HERMES_AGENT_ROOT) { $candidates += $env:HERMES_AGENT_ROOT }
  if ($env:LOCALAPPDATA) {
    $candidates += (Join-Path $env:LOCALAPPDATA 'hermes\hermes-agent')
  }
  # Legacy / alternate layouts some users keep
  if ($env:USERPROFILE) {
    $candidates += (Join-Path $env:USERPROFILE 'AppData\Local\hermes\hermes-agent')
    $candidates += (Join-Path $env:USERPROFILE 'hermes-agent')
    $candidates += (Join-Path $env:USERPROFILE 'hermes\hermes-agent')
  }

  foreach ($c in $candidates) {
    if (-not $c) { continue }
    try { $full = [System.IO.Path]::GetFullPath($c) } catch { continue }
    $desktopPkg = Join-Path $full 'apps\desktop\package.json'
    if ((Test-Path (Join-Path $full '.git')) -or (Test-Path $desktopPkg)) {
      if (Test-Path $desktopPkg) { return $full }
    }
  }
  return $null
}

function Resolve-ModFile {
  param([string]$RelativePath)
  # Prefer package/files/<name> (repo layout). Flat zip root is also accepted.
  $a = Join-Path $PSScriptRoot $RelativePath
  if (Test-Path $a) { return $a }
  $leaf = Split-Path $RelativePath -Leaf
  $b = Join-Path $PSScriptRoot $leaf
  if (Test-Path $b) { return $b }
  return $null
}

$root = Resolve-HermesRoot -Explicit $Root
if (-not $root) {
  Write-Host "ОШИБКА: не найден клон hermes-agent."
  Write-Host "  Ожидается apps\desktop\package.json в одном из путей:"
  Write-Host "  - %LOCALAPPDATA%\hermes\hermes-agent"
  Write-Host "  - \$env:HERMES_AGENT_ROOT"
  Write-Host "  Или передайте: install.ps1 -Root 'D:\path\to\hermes-agent'"
  exit 1
}

$desktop = Join-Path $root 'apps\desktop'
$res = Join-Path $desktop 'release\win-unpacked\resources'
$asar = Join-Path $res 'app.asar'
$asarJs = Join-Path $root 'node_modules\@electron\asar\bin\asar.js'
$modDist = Join-Path $PSScriptRoot 'dist'
$tmp = Join-Path $env:TEMP ('asar-mod-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
$app = Join-Path $tmp 'app'
$unpacked = Join-Path $res 'app.asar.unpacked'
$expectFile = Join-Path $PSScriptRoot 'EXPECTED_COMMIT'
$registry = Join-Path $PSScriptRoot 'registry.json'
$probeJs = Join-Path $PSScriptRoot 'probe-ru.mjs'

Write-Host "== Hermes Desktop RU — установщик v1.0.1 =="
Write-Host ("клон: " + $root)
if (-not (Test-Path $registry)) {
  Write-Host "ОШИБКА: registry.json не найден рядом с установщиком"
  exit 1
}

# ---------- deps health ----------
$healthBad = $false
node (Join-Path $PSScriptRoot 'deps-health.mjs') $root
if ($LASTEXITCODE -ne 0) { $healthBad = $true }
if ($healthBad) {
  if (Test-Path (Join-Path $root 'package-lock.json')) {
    Write-Host "зависимости повреждены — npm ci (3–10 мин)..."
    Push-Location $root
    cmd /c "npm ci 2>&1"
    Pop-Location
  } else {
    Write-Host "зависимости повреждены — npm install..."
    Push-Location $root
    cmd /c "npm install 2>&1"
    Pop-Location
  }
  node (Join-Path $PSScriptRoot 'deps-health.mjs') $root
  if ($LASTEXITCODE -ne 0) {
    Write-Host "ОШИБКА: после переустановки node_modules пакеты всё ещё отсутствуют (проверьте сеть/npm)"
    exit 1
  }
  Write-Host "зависимости восстановлены"
} else {
  Write-Host "зависимости: OK"
}
if (-not (Test-Path $asarJs)) {
  Write-Host "ОШИБКА: @electron/asar не найден после шага зависимостей"
  exit 1
}

Get-Process -Name Hermes -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# ---------- version-gate ----------
$actualCommit = ""
Push-Location $root
$actualCommit = (& cmd /c "git rev-parse HEAD 2>nul")
Pop-Location
if (-not $actualCommit) { $actualCommit = "(git недоступен?)" }
if (Test-Path $expectFile) {
  $expectedCommit = (Get-Content $expectFile -Raw).Trim()
  $aShort = $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length))
  $eShort = $expectedCommit.Substring(0, [Math]::Min(12, $expectedCommit.Length))
  Write-Host ("версия клона: " + $aShort + "  (ожидалась " + $eShort + ")")
  $aTrim = "$actualCommit".Trim()
  $match = ($aTrim -eq $expectedCommit) -or $aTrim.StartsWith($expectedCommit) -or $expectedCommit.StartsWith($aTrim.Substring(0, [Math]::Min(7, $aTrim.Length)))
  if (-not $match) {
    Write-Host "ПРЕДУПРЕЖДЕНИЕ: HEAD клона отличается от версии, на которой собран реестр."
    Write-Host "  Реальный контроль — doctor ниже. Если он 100% OK, мод всё ещё совместим."
  } else {
    Write-Host "версия: совпадает с ожидаемой"
  }
} else {
  Write-Host ("version-gate: EXPECTED_COMMIT нет (HEAD=" + $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length)) + ")")
}

# ---------- restore tracked to stock ----------
Push-Location $root
cmd /c "git restore --source=HEAD --staged --worktree . 2>nul"
$restoreExit = $LASTEXITCODE
Pop-Location
Write-Host ("сброс к стоку: exit=" + $restoreExit + " (untracked-локали не трогаем)")

# ---------- doctor ----------
Push-Location $root
node (Join-Path $PSScriptRoot 'apply-hardcodes.mjs') $root $registry --doctor
$doctorExit = $LASTEXITCODE
Pop-Location
if ($doctorExit -ne 0) {
  Write-Host "ОШИБКА: doctor — часть правил реестра не применяется к этой версии Hermes."
  Write-Host "  Скачайте свежий релиз мода или обновите registry/overrides."
  if ($Doctor) {
    Write-Host ""
    Write-Host "=== ОТЧЁТ DOCTOR ==="
    Write-Host ("HEAD клона : " + $actualCommit)
    Write-Host ("реестр     : " + $registry)
    Write-Host "статус: FAIL"
    exit 1
  }
  exit 1
} else {
  Write-Host "doctor: 100% правил применяются"
}
if ($Doctor) {
  Write-Host ""
  Write-Host "=== ОТЧЁТ DOCTOR ==="
  Write-Host ("HEAD клона : " + $actualCommit)
  Write-Host ("реестр     : " + $registry)
  Write-Host "статус: OK (сухой прогон, ничего не записано)"
  exit 0
}

# ---------- apply ----------
Push-Location $root
node (Join-Path $PSScriptRoot 'apply-hardcodes.mjs') $root $registry
$applyExit = $LASTEXITCODE
Pop-Location
if ($applyExit -ne 0) { Write-Host "ОШИБКА: apply реестра прерван"; exit 1 }
Write-Host "apply: реестр применён"

# ---------- locale files (files/ layout OR flat zip root) ----------
$fileMap = @(
  @('files\ru.ts', 'apps\desktop\src\i18n\ru.ts'),
  @('files\ru-constants.ts', 'apps\desktop\src\app\settings\ru-constants.ts'),
  @('files\ru-locales.ts', 'apps\desktop\src\plugins\kanban\ru-locales.ts')
)
$copied = 0
foreach ($f in $fileMap) {
  $src = Resolve-ModFile $f[0]
  $dst = Join-Path $root $f[1]
  if ($src) {
    $dir = Split-Path $dst -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Copy-Item $src $dst -Force
    Write-Host ("локаль: " + $f[1])
    $copied++
  } else {
    Write-Host ("ПРЕДУПРЕЖДЕНИЕ: не найден файл мода " + $f[0] + " (и плоский fallback)")
  }
}
if ($copied -lt 1) {
  Write-Host "ОШИБКА: ни один locale-файл мода не найден рядом с установщиком"
  exit 1
}

# ---------- backups ----------
if ((Test-Path $asar) -and -not (Test-Path ($asar + '.stock.bak'))) {
  Copy-Item $asar ($asar + '.stock.bak')
}
if ((Test-Path (Join-Path $unpacked 'dist')) -and -not (Test-Path (Join-Path $unpacked 'dist.stock.bak'))) {
  Copy-Item (Join-Path $unpacked 'dist') (Join-Path $unpacked 'dist.stock.bak') -Recurse
}
Write-Host "бэкапы: OK"

# ---------- structural i18n ----------
$i18nDir = Join-Path $root 'apps\desktop\src\i18n'
$struct = Join-Path $PSScriptRoot 'structural-i18n.mjs'
if (Test-Path $struct) {
  node $struct $i18nDir
  if ($LASTEXITCODE -ne 0) { Write-Host "ОШИБКА: structural-i18n"; exit 1 }
  Write-Host "регистрация ru: OK"
} else {
  Write-Host "ПРЕДУПРЕЖДЕНИЕ: structural-i18n.mjs отсутствует — язык ru может не попасть в бандл"
}

# ---------- build ----------
Write-Host "сборка dist (npm run build, 5–10 мин)..."
Push-Location $desktop
$buildLog = Join-Path $env:TEMP 'mod-build.log'
cmd /c ("npm run build > `"" + $buildLog + "`" 2>&1")
$buildExit = $LASTEXITCODE
Pop-Location
$usePackage = $false
if ($buildExit -ne 0) {
  Write-Host ("ПРЕДУПРЕЖДЕНИЕ: npm run build failed (exit " + $buildExit + ") — см. " + $buildLog)
  if (Test-Path (Join-Path $modDist 'index.html')) {
    Write-Host "fallback: package dist/"
    $usePackage = $true
  } else {
    Write-Host "ОШИБКА: нет ни успешной сборки, ни package dist/"
    exit 1
  }
} else {
  Write-Host "сборка: OK"
}

# ---------- asar rebuild ----------
if (-not (Test-Path $asar)) {
  Write-Host "ОШИБКА: не найден packaged app.asar:"
  Write-Host ("  " + $asar)
  Write-Host "  Сначала соберите Desktop: cd apps\desktop && npm run pack"
  exit 1
}

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
if ($LASTEXITCODE -ne 0) { Write-Host "ОШИБКА: extract asar"; exit 1 }

if ($usePackage) { $srcDist = $modDist } else { $srcDist = Join-Path $desktop 'dist' }
if (Test-Path (Join-Path $app 'dist')) { Remove-Item (Join-Path $app 'dist') -Recurse -Force }
Copy-Item $srcDist (Join-Path $app 'dist') -Recurse
Write-Host ("dist из: " + $(if ($usePackage) { 'package' } else { 'clone build' }))

if (Test-Path $unpacked) { Remove-Item $unpacked -Recurse -Force }
node $asarJs pack $app $asar --unpack "**" | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "ОШИБКА: pack asar"; exit 1 }

# ---------- checks ----------
$physIndex = Test-Path (Join-Path $unpacked 'dist\index.html')
$physMain = Test-Path (Join-Path $unpacked 'dist\electron-main.mjs')
$physPkg = Test-Path (Join-Path $unpacked 'package.json')
$ruMarker = 'нет'
$assetsDir = Join-Path $unpacked 'dist\assets'
if ((Test-Path $assetsDir) -and (Test-Path $probeJs)) {
  $ru = node $probeJs $assetsDir
  if ($ru -and $ru -ne 'NONE') { $ruMarker = 'FOUND (' + $ru + ')' }
} elseif (-not (Test-Path $probeJs)) {
  Write-Host "ПРЕДУПРЕЖДЕНИЕ: probe-ru.mjs отсутствует — пропускаю проверку маркера"
}
Write-Host ("проверки: index=" + $physIndex + " main=" + $physMain + " pkg=" + $physPkg + " ru=" + $ruMarker)
if (-not ($physIndex -and $physMain -and $physPkg)) {
  Write-Host "ОШИБКА: проверки упаковки провалены — восстановите app.asar.stock.bak"
  exit 1
}
if ($ruMarker -eq 'нет') {
  Write-Host "ПРЕДУПРЕЖДЕНИЕ: RU-маркер не найден — мод мог не попасть в бандл"
}

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "УСТАНОВКА OK — перезапустите Hermes Desktop"
