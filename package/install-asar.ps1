param(
  [switch]$Doctor,
  [switch]$Help,
  [switch]$Uninstall,
  [switch]$AllowStaleDist,
  [switch]$Version,
  [string]$Root
)

$ErrorActionPreference = 'Stop'
# install-asar.ps1 v1.1.0 + gate 24.08 — cosmetic AMBIGUOUS no longer FAIL
# Structural anchor registry installer for hermes-desktop-ru.
# Pure logic in ASCII identifiers; user-facing messages may be Russian (UTF-8 BOM required).

function Get-ModVersion {
  $candidates = @(
    (Join-Path $PSScriptRoot '..\package.json'),
    (Join-Path $PSScriptRoot 'package.json')
  )
  foreach ($p in $candidates) {
    if (Test-Path $p) {
      try {
        $j = Get-Content $p -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($j.version) { return [string]$j.version }
      } catch { }
    }
  }
  return '1.1.0'
}

function Show-Help {
  $ver = Get-ModVersion
  @"
Hermes Desktop RU - установщик мода v$ver

Использование:
  install.ps1                      Установить / переустановить мод
  install.ps1 -Doctor              Сухая проверка совместимости (ничего не пишет)
  install.ps1 -Uninstall           Откатить packaged app.asar из .stock.bak
  install.ps1 -Root <path>         Явный путь к клону hermes-agent
  install.ps1 -AllowStaleDist      Если npm run build упал — взять package/dist (иначе ошибка)
  install.ps1 -Help                Эта справка

CLI (npm):
  hermes-desktop-ru install | doctor | uninstall | version | help

Также можно:
  install.bat                      То же через двойной клик (с паузой в конце)
  $env:HERMES_AGENT_ROOT           Переопределить путь к клону

Требования:
  - Hermes Desktop из исходников (git clone), не prebuilt .exe
  - Node.js 18+ и npm
  - Закрытый Hermes Desktop на время установки / отката

По умолчанию ищет клон в:
  %LOCALAPPDATA%\hermes\hermes-agent

Важно:
  - doctor ничего не убивает и не делает git restore
  - install откатывает tracked-исходники клона к HEAD (другие патчи в клоне не живут)
  - uninstall трогает только app.asar (+ dist.stock.bak), не клон
  - косметический MISSING/AMBIGUOUS (в т.ч. Bots) не стопорит установку
  - FAIL только если пропал файл критичного правила; сборка — отдельный стоп
"@ | Write-Host
}

if ($Help) { Show-Help; exit 0 }
if ($Version) { Write-Host (Get-ModVersion); exit 0 }

if ($Doctor -and $Uninstall) {
  Write-Host "ОШИБКА: -Doctor и -Uninstall вместе нельзя"
  exit 2
}

function Resolve-HermesRoot {
  param([string]$Explicit)
  $candidates = @()
  if ($Explicit) { $candidates += $Explicit }
  if ($env:HERMES_AGENT_ROOT) { $candidates += $env:HERMES_AGENT_ROOT }
  if ($env:LOCALAPPDATA) {
    $candidates += (Join-Path $env:LOCALAPPDATA 'hermes\hermes-agent')
  }
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
  $a = Join-Path $PSScriptRoot $RelativePath
  if (Test-Path $a) { return $a }
  $leaf = Split-Path $RelativePath -Leaf
  $b = Join-Path $PSScriptRoot $leaf
  if (Test-Path $b) { return $b }
  return $null
}

function Stop-HermesRelated {
  param([string]$CloneRoot)
  $killed = @()
  foreach ($n in @('Hermes', 'hermes')) {
    Get-Process -Name $n -ErrorAction SilentlyContinue | ForEach-Object {
      $killed += ($_.ProcessName + ':' + $_.Id)
      Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
  }
  if ($CloneRoot) {
    $rootNorm = $CloneRoot.TrimEnd('\').ToLowerInvariant()
    Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
      $p = $null
      try { $p = $_.Path } catch { return }
      if (-not $p) { return }
      $pl = $p.ToLowerInvariant()
      if ($pl.StartsWith($rootNorm) -or $pl.Contains('\hermes\hermes-agent\')) {
        $killed += ($_.ProcessName + ':' + $_.Id)
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
      }
    }
  }
  $uniq = $killed | Select-Object -Unique
  if ($uniq) {
    Write-Host ("остановлены процессы: " + ($uniq -join ', '))
    Start-Sleep -Seconds 2
  } else {
    Write-Host "процессы Hermes не найдены (ок)"
  }
}

function Show-VersionGate {
  param([string]$RootPath, [string]$ExpectFile)
  $actualCommit = ""
  Push-Location $RootPath
  $actualCommit = (& cmd /c "git rev-parse HEAD 2>nul")
  Pop-Location
  if (-not $actualCommit) { $actualCommit = "(git недоступен?)" }
  if (Test-Path $ExpectFile) {
    $expectedCommit = (Get-Content $ExpectFile -Raw).Trim()
    $aShort = $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length))
    $eShort = $expectedCommit.Substring(0, [Math]::Min(12, $expectedCommit.Length))
    Write-Host ("версия клона: " + $aShort + "  (ожидалась " + $eShort + ")")
    $aTrim = "$actualCommit".Trim()
    $match = ($aTrim -eq $expectedCommit) -or $aTrim.StartsWith($expectedCommit) -or $expectedCommit.StartsWith($aTrim.Substring(0, [Math]::Min(7, $aTrim.Length)))
    if (-not $match) {
      Write-Host "ПРЕДУПРЕЖДЕНИЕ: HEAD клона отличается от версии, на которой собран реестр."
      Write-Host "  Реальный контроль — doctor. Косметический WARN не значит «несовместим»."
    } else {
      Write-Host "версия: совпадает с ожидаемой"
    }
  } else {
    Write-Host ("version-gate: EXPECTED_COMMIT нет (HEAD=" + $actualCommit.Substring(0, [Math]::Min(12, $actualCommit.Length)) + ")")
  }
  return $actualCommit
}

function Invoke-DoctorCheck {
  param([string]$RootPath, [string]$RegistryPath)
  Push-Location $RootPath
  $script:doctorOutput = & node (Join-Path $PSScriptRoot 'apply-hardcodes.mjs') $RootPath $RegistryPath --doctor 2>&1
  $script:doctorExit = $LASTEXITCODE
  Pop-Location
  if ($script:doctorOutput) { $script:doctorOutput | ForEach-Object { Write-Host $_ } }

  $script:crMissFile = 0
  $script:crMiss = 0
  $script:crAmb = 0
  $script:cosMiss = 0
  $script:cosAmb = 0
  foreach ($line in $script:doctorOutput) {
    $s = [string]$line
    if ($s -match 'GATE critical_missing_file=(\d+) critical_missing=(\d+) critical_ambiguous=(\d+) cosmetic_missing=(\d+) cosmetic_ambiguous=(\d+)') {
      $script:crMissFile = [int]$Matches[1]
      $script:crMiss = [int]$Matches[2]
      $script:crAmb = [int]$Matches[3]
      $script:cosMiss = [int]$Matches[4]
      $script:cosAmb = [int]$Matches[5]
    }
  }
}

function Test-DoctorShouldFail {
  return ($script:crMissFile -gt 0)
}

function Write-DoctorStatus {
  param([switch]$AsInstall)
  if ($script:crMissFile -gt 0) {
    if ($AsInstall) {
      Write-Host "ОШИБКА: doctor — пропал файл критичного правила реестра."
      Write-Host "  Апстрим убрал kanban или connection-registry. Скачайте свежий релиз мода или обновите registry/overrides."
    } else {
      Write-Host "статус: FAIL"
      Write-Host "  Пропал файл критичного правила (обычно kanban/plugin.tsx или connection-registry.ts)."
    }
    return
  }
  if ($script:crMiss -gt 0 -or $script:crAmb -gt 0) {
    $n = $script:crMiss + $script:crAmb
    if ($AsInstall) {
      Write-Host ("ПРЕДУПРЕЖДЕНИЕ: " + $n + " критичных правил не применились — фичи мода, зависящие от них, будут отключены.")
      Write-Host "  Установка продолжается (эти места останутся в поведении Hermes как в апстриме)."
    } else {
      Write-Host ("статус: WARN (установка возможна, " + $n + " критичных фич отключено)")
    }
    return
  }
  if ($AsInstall) {
    Write-Host "doctor: критичные правила — все на месте"
    if ($script:cosMiss -gt 0 -or $script:cosAmb -gt 0) {
      Write-Host ("ПРЕДУПРЕЖДЕНИЕ: косметика missing=" + $script:cosMiss + " ambiguous=" + $script:cosAmb + " (см. PROBLEMS) — затронутые места останутся на английском.")
    }
  } else {
    if ($script:cosMiss -gt 0 -or $script:cosAmb -gt 0) {
      Write-Host ("статус: WARN (косметика missing=" + $script:cosMiss + " ambiguous=" + $script:cosAmb + " — эти места останутся на английском, установка идёт)")
    } else {
      Write-Host "статус: OK (сухой прогон, ничего не записано)"
    }
  }
}

$modVer = Get-ModVersion
$root = Resolve-HermesRoot -Explicit $Root
if (-not $root) {
  Write-Host "ОШИБКА: не найден клон hermes-agent."
  Write-Host "  Ожидается apps\desktop\package.json в одном из путей:"
  Write-Host "  - %LOCALAPPDATA%\hermes\hermes-agent"
  Write-Host "  - `$env:HERMES_AGENT_ROOT"
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

Write-Host ("== Hermes Desktop RU — установщик v" + $modVer + " ==")
Write-Host ("клон: " + $root)

# ---------- uninstall (asar only, clone untouched) ----------
if ($Uninstall) {
  Stop-HermesRelated -CloneRoot $root
  $bak = $asar + '.stock.bak'
  if (-not (Test-Path $bak)) {
    Write-Host "ОШИБКА: нет app.asar.stock.bak — нечего откатывать."
    Write-Host ("  Ожидался файл: " + $bak)
    Write-Host "  Его создаёт install при первой установке. Полный сброс — hermes update."
    exit 1
  }
  Copy-Item $bak $asar -Force
  Write-Host "app.asar восстановлен из .stock.bak"
  $distBak = Join-Path $unpacked 'dist.stock.bak'
  $distLive = Join-Path $unpacked 'dist'
  if (Test-Path $distBak) {
    if (Test-Path $distLive) { Remove-Item $distLive -Recurse -Force -ErrorAction SilentlyContinue }
    Copy-Item $distBak $distLive -Recurse -Force
    Write-Host "app.asar.unpacked\dist восстановлен из dist.stock.bak"
  }
  Write-Host "ОТКАТ OK — packaged Desktop снова стоковый."
  Write-Host "  Исходники клона не трогались. Полный сброс клона — hermes update."
  exit 0
}

if (-not (Test-Path $registry)) {
  Write-Host "ОШИБКА: registry.json не найден рядом с установщиком"
  exit 1
}

# ---------- doctor (truly dry: no kill, no git restore, no npm ci) ----------
if ($Doctor) {
  Push-Location $root
  $dirty = & cmd /c "git status --porcelain --untracked-files=no 2>nul"
  Pop-Location
  if ($dirty) {
    Write-Host "ПРЕДУПРЕЖДЕНИЕ: в клоне есть локальные правки tracked-файлов."
    Write-Host "  Doctor проверяет ТЕКУЩЕЕ дерево и ничего не откатывает."
    Write-Host "  Для проверки против стока сначала: git restore --source=HEAD --staged --worktree ."
  }
  $actualCommit = Show-VersionGate -RootPath $root -ExpectFile $expectFile
  Invoke-DoctorCheck -RootPath $root -RegistryPath $registry
  Write-Host ""
  Write-Host "=== ОТЧЁТ DOCTOR ==="
  Write-Host ("HEAD клона : " + $actualCommit)
  Write-Host ("реестр     : " + $registry)
  Write-DoctorStatus
  if (Test-DoctorShouldFail) { exit 1 }
  exit 0
}

# ---------- install only below ----------

# deps health + repair (writes node_modules — install only)
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

Stop-HermesRelated -CloneRoot $root

$actualCommit = Show-VersionGate -RootPath $root -ExpectFile $expectFile

# restore tracked to stock — INSTALL ONLY
Push-Location $root
cmd /c "git restore --source=HEAD --staged --worktree . 2>nul"
$restoreExit = $LASTEXITCODE
Pop-Location
Write-Host ("сброс к стоку: exit=" + $restoreExit + " (untracked-локали не трогаем)")

Invoke-DoctorCheck -RootPath $root -RegistryPath $registry

if (Test-DoctorShouldFail) {
  Write-DoctorStatus -AsInstall
  exit 1
}
Write-DoctorStatus -AsInstall

# ---------- apply ----------
Push-Location $root
node (Join-Path $PSScriptRoot 'apply-hardcodes.mjs') $root $registry
$applyExit = $LASTEXITCODE
Pop-Location
if ($applyExit -ne 0) { Write-Host "ОШИБКА: apply реестра прерван (пропал файл критичного правила)"; exit 1 }
Write-Host "apply: реестр применён (косметические пропуски, если были, оставлены как есть)"

# ---------- locale files ----------
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
  Write-Host ("ОШИБКА: npm run build failed (exit " + $buildExit + ") — см. " + $buildLog)
  if ($AllowStaleDist -and (Test-Path (Join-Path $modDist 'index.html'))) {
    Write-Host "ПРЕДУПРЕЖДЕНИЕ: -AllowStaleDist — беру package/dist (может не совпасть с этим апстримом)"
    $usePackage = $true
  } else {
    Write-Host "  Повтор с устаревшим package/dist отключён (иначе «УСТАНОВКА OK» со старым UI)."
    Write-Host "  Если очень надо: install.ps1 -AllowStaleDist"
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
Write-Host ("dist из: " + $(if ($usePackage) { 'package (stale, -AllowStaleDist)' } else { 'clone build' }))

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