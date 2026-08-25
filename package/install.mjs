#!/usr/bin/env node
// install.mjs — кроссплатформенный установщик hermes-desktop-ru.
// Источник истины. PowerShell / BAT / sh — тонкие обёртки.
//
// Команды: install | doctor | uninstall | version | help | --self-test
// Флаги: --root <path> | --allow-stale-dist
//
// Резолв клона: --root → HERMES_AGENT_ROOT → HERMES_INSTALL_DIR →
//   $HERMES_HOME/hermes-agent → ~/.hermes/hermes-agent →
//   /usr/local/lib/hermes-agent → %LOCALAPPDATA%\hermes\hermes-agent
// Резолв asar: только apps/desktop/release/{win-unpacked,linux-unpacked,mac*/Hermes.app}
//   Официальный notarized .app из /Applications и AppImage с сайта — не трогаем.
//
// Linux/macOS — экспериментально. Автор мода на них установку не гонял.
// Kill/uninstall на unix — best-effort, не обещаем качество Windows.
import { spawnSync } from 'node:child_process'
import {
  existsSync,
  readFileSync,
  writeFileSync,
  copyFileSync,
  mkdirSync,
  rmSync,
  cpSync,
  readdirSync,
  mkdtempSync,
  openSync,
  closeSync,
} from 'node:fs'
import { tmpdir, homedir } from 'node:os'
import path from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const isWin = process.platform === 'win32'
const isMac = process.platform === 'darwin'
const isLinux = process.platform === 'linux'
const FALLBACK_VERSION = '1.2.0'

function sleepSync(ms) {
  const buf = new Int32Array(new SharedArrayBuffer(4))
  Atomics.wait(buf, 0, 0, ms)
}

function readVersion() {
  const candidates = [
    path.join(here, '..', 'package.json'),
    path.join(here, 'package.json'),
  ]
  for (const p of candidates) {
    try {
      if (!existsSync(p)) continue
      const j = JSON.parse(readFileSync(p, 'utf8'))
      if (j.version) return String(j.version)
    } catch {
      /* ignore */
    }
  }
  return FALLBACK_VERSION
}

function showHelp() {
  const ver = readVersion()
  const text = `Hermes Desktop RU — установщик мода v${ver}

Использование:
  node install.mjs                    установить / переустановить
  node install.mjs doctor             сухая проверка (ничего не пишет)
  node install.mjs uninstall          откатить app.asar из .stock.bak
  node install.mjs version            версия пакета
  node install.mjs --self-test        проверка установщика без клона Hermes
  node install.mjs --root <path>      явный путь к клону hermes-agent
  node install.mjs --allow-stale-dist если npm run build упал — взять package/dist
  node install.mjs help               эта справка

CLI (npm):
  hermes-desktop-ru install | doctor | uninstall | version | help

Обёртки:
  install.bat / install.ps1           Windows, в т.ч. двойной клик
  install.sh                          Linux / macOS

Требования:
  - Hermes Desktop из исходников (git clone / hermes desktop), не prebuilt
  - Node.js 18+ и npm
  - На время install/uninstall лучше закрыть Desktop

Где ищем клон:
  --root  ·  HERMES_AGENT_ROOT  ·  HERMES_INSTALL_DIR
  $HERMES_HOME/hermes-agent
  ~/.hermes/hermes-agent
  /usr/local/lib/hermes-agent          (root-install на Linux)
  %LOCALAPPDATA%\\hermes\\hermes-agent (Windows)

Где ищем app.asar (только внутри клона, не /Applications):
  apps/desktop/release/win-unpacked/resources/app.asar
  apps/desktop/release/linux-unpacked/resources/app.asar
  apps/desktop/release/mac[-arm64|-x64]/Hermes.app/Contents/Resources/app.asar

Важно:
  - doctor ничего не убивает и не делает git restore
  - install откатывает tracked-исходники клона к HEAD (другие патчи в клоне не живут)
  - uninstall трогает только app.asar (+ dist.stock.bak), не клон
  - косметический MISSING/AMBIGUOUS (в т.ч. Bots) не стопорит установку
  - FAIL только если пропал файл критичного правила; сборка — отдельный стоп
  - Linux/macOS: экспериментально, автор не тестировал. Не ставьте мод
    в официальный подписанный .app с сайта — только self-built из клона.
`
  process.stdout.write(text)
}

function failUnknown(flag) {
  console.error(`Неизвестный аргумент: ${flag}`)
  console.error('Справка: node install.mjs help')
  process.exit(2)
}

function parseArgs(argv) {
  const out = {
    cmd: 'install',
    root: null,
    allowStaleDist: false,
  }
  const args = [...argv]
  if (args[0] && !args[0].startsWith('-')) {
    const c = args.shift().toLowerCase()
    const map = {
      install: 'install',
      doctor: 'doctor',
      uninstall: 'uninstall',
      version: 'version',
      help: 'help',
      'self-test': 'self-test',
      selftest: 'self-test',
    }
    if (!map[c]) {
      console.error(`Неизвестная команда: ${c}. Доступно: install, doctor, uninstall, version, help`)
      process.exit(2)
    }
    out.cmd = map[c]
  }
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    const raw = a.replace(/^--?/, '')
    const al = raw.toLowerCase()
    if (al === 'doctor') out.cmd = 'doctor'
    else if (al === 'uninstall') out.cmd = 'uninstall'
    else if (al === 'help' || al === 'h') out.cmd = 'help'
    else if (al === 'version' || al === 'v') out.cmd = 'version'
    else if (al === 'self-test' || al === 'selftest') out.cmd = 'self-test'
    else if (al === 'allowstaledist' || al === 'allow-stale-dist') out.allowStaleDist = true
    else if (al === 'root') {
      const v = args[++i]
      if (!v || v.startsWith('-')) {
        console.error('ОШИБКА: --root требует путь')
        process.exit(2)
      }
      out.root = v
    } else if (al.startsWith('root=')) {
      out.root = raw.slice(raw.indexOf('=') + 1)
    } else {
      failUnknown(a)
    }
  }
  return out
}

function isHermesClone(dir) {
  if (!dir) return false
  return existsSync(path.join(dir, 'apps', 'desktop', 'package.json'))
}

function uniqueResolved(list) {
  const seen = new Set()
  const out = []
  for (const c of list) {
    if (!c) continue
    let full
    try {
      full = path.resolve(c)
    } catch {
      continue
    }
    const key = full.replace(/\\/g, '/').toLowerCase()
    if (seen.has(key)) continue
    seen.add(key)
    out.push(full)
  }
  return out
}

function rootCandidates(explicit) {
  const home = homedir()
  const list = [
    explicit,
    process.env.HERMES_AGENT_ROOT,
    process.env.HERMES_INSTALL_DIR,
    process.env.HERMES_HOME ? path.join(process.env.HERMES_HOME, 'hermes-agent') : null,
    path.join(home, '.hermes', 'hermes-agent'),
    '/usr/local/lib/hermes-agent',
    process.env.LOCALAPPDATA
      ? path.join(process.env.LOCALAPPDATA, 'hermes', 'hermes-agent')
      : null,
    path.join(home, 'AppData', 'Local', 'hermes', 'hermes-agent'),
    path.join(home, 'hermes-agent'),
    path.join(home, 'hermes', 'hermes-agent'),
  ]
  return uniqueResolved(list)
}

function resolveHermesRoot(explicit) {
  for (const c of rootCandidates(explicit)) {
    if (isHermesClone(c)) return c
  }
  return null
}

function normPath(p) {
  return path.resolve(p).replace(/\\/g, '/').toLowerCase()
}

function pathInside(child, parent) {
  if (!child || !parent) return false
  const c = normPath(child)
  const p = normPath(parent)
  return c === p || c.startsWith(p.endsWith('/') ? p : `${p}/`)
}

function scorePack(resources) {
  const n = resources.replace(/\\/g, '/')
  let s = 0
  if (isWin && n.includes('/win-unpacked/')) s += 20
  if (isLinux && n.includes('/linux-unpacked/')) s += 20
  if (isMac && /Hermes\.app\/Contents\/Resources$/i.test(n)) s += 20
  if (isMac && n.includes('/mac-arm64/') && process.arch === 'arm64') s += 6
  if (isMac && n.includes('/mac-x64/') && process.arch === 'x64') s += 6
  if (n.includes('/win-unpacked/')) s += 2
  if (n.includes('/linux-unpacked/')) s += 2
  if (/Hermes\.app\/Contents\/Resources$/i.test(n)) s += 2
  return s
}

function collectPacks(releaseDir) {
  const found = []
  const seen = new Set()
  function add(resources) {
    const asar = path.join(resources, 'app.asar')
    if (!existsSync(asar)) return
    const key = normPath(resources)
    if (seen.has(key)) return
    seen.add(key)
    found.push({
      resources,
      asar,
      unpacked: path.join(resources, 'app.asar.unpacked'),
    })
  }

  add(path.join(releaseDir, 'win-unpacked', 'resources'))
  add(path.join(releaseDir, 'linux-unpacked', 'resources'))
  add(path.join(releaseDir, 'mac-arm64', 'Hermes.app', 'Contents', 'Resources'))
  add(path.join(releaseDir, 'mac', 'Hermes.app', 'Contents', 'Resources'))
  add(path.join(releaseDir, 'mac-x64', 'Hermes.app', 'Contents', 'Resources'))
  add(path.join(releaseDir, 'Hermes.app', 'Contents', 'Resources'))

  function walk(dir, depth) {
    if (depth > 4) return
    let ents
    try {
      ents = readdirSync(dir, { withFileTypes: true })
    } catch {
      return
    }
    for (const e of ents) {
      if (!e.isDirectory()) continue
      const p = path.join(dir, e.name)
      if (e.name === 'Resources') add(p)
      else walk(p, depth + 1)
    }
  }
  if (existsSync(releaseDir)) walk(releaseDir, 0)
  return found
}

function resolvePack(root) {
  const release = path.join(root, 'apps', 'desktop', 'release')
  const found = collectPacks(release)
  if (!found.length) return null
  found.sort((a, b) => scorePack(b.resources) - scorePack(a.resources))
  return found[0]
}

function resolveModFile(rel) {
  const a = path.join(here, rel)
  if (existsSync(a)) return a
  const b = path.join(here, path.basename(rel))
  if (existsSync(b)) return b
  return null
}

function run(cmd, args, opts = {}) {
  return spawnSync(cmd, args, {
    cwd: opts.cwd,
    input: opts.input,
    stdio: opts.stdio ?? 'pipe',
    encoding: opts.stdio === 'inherit' ? undefined : 'utf8',
    windowsHide: true,
    shell: opts.shell ?? false,
  })
}

function runGit(root, args) {
  return run('git', args, { cwd: root })
}

function runNpm(args, cwd, inherit = true) {
  const cmd = isWin ? 'npm.cmd' : 'npm'
  // npm на Windows — это .cmd (batch), spawnSync без shell даёт EINVAL
  return run(cmd, args, { cwd, stdio: inherit ? 'inherit' : 'pipe', shell: isWin })
}

function shortSha(s, n = 12) {
  const t = String(s || '').trim()
  return t.slice(0, Math.min(n, t.length)) || '?'
}

function showVersionGate(root, expectFile) {
  let actual = ''
  const r = runGit(root, ['rev-parse', 'HEAD'])
  if (r.error) {
    actual = '(git недоступен?)'
  } else if (r.status !== 0) {
    actual = (r.stderr || r.stdout || '(git недоступен?)').trim() || '(git недоступен?)'
  } else {
    actual = (r.stdout || '').trim()
  }
  if (existsSync(expectFile)) {
    const expected = readFileSync(expectFile, 'utf8').trim()
    console.log(`версия клона: ${shortSha(actual)}  (ожидалась ${shortSha(expected)})`)
    const aTrim = actual.trim()
    const prefix = aTrim.slice(0, Math.min(7, aTrim.length))
    const match =
      aTrim === expected ||
      aTrim.startsWith(expected) ||
      (prefix && expected.startsWith(prefix))
    if (!match) {
      console.log('ПРЕДУПРЕЖДЕНИЕ: HEAD клона отличается от версии, на которой собран реестр.')
      console.log('  Реальный контроль — doctor. Косметический WARN не значит «несовместим».')
    } else {
      console.log('версия: совпадает с ожидаемой')
    }
  } else {
    console.log(`version-gate: EXPECTED_COMMIT нет (HEAD=${shortSha(actual)})`)
  }
  return actual
}

function parseGate(output) {
  const gate = {
    crMissFile: 0,
    crMiss: 0,
    crAmb: 0,
    cosMiss: 0,
    cosAmb: 0,
    found: false,
  }
  const re =
    /GATE critical_missing_file=(\d+) critical_missing=(\d+) critical_ambiguous=(\d+) cosmetic_missing=(\d+) cosmetic_ambiguous=(\d+)/
  for (const line of String(output).split(/\r?\n/)) {
    const m = line.match(re)
    if (!m) continue
    gate.crMissFile = Number(m[1])
    gate.crMiss = Number(m[2])
    gate.crAmb = Number(m[3])
    gate.cosMiss = Number(m[4])
    gate.cosAmb = Number(m[5])
    gate.found = true
  }
  return gate
}

function invokeDoctor(root, registry) {
  const applyJs = path.join(here, 'apply-hardcodes.mjs')
  if (!existsSync(applyJs)) {
    console.error('ОШИБКА: apply-hardcodes.mjs не найден рядом с установщиком')
    process.exit(1)
  }
  const r = run(process.execPath, [applyJs, root, registry, '--doctor'], { cwd: root })
  const output = `${r.stdout || ''}${r.stderr || ''}`
  if (output) process.stdout.write(output.endsWith('\n') ? output : `${output}\n`)
  if (r.error) {
    console.error(`ОШИБКА: не удалось запустить doctor: ${r.error.message}`)
    process.exit(1)
  }
  const gate = parseGate(output)
  if (!gate.found) {
    console.error('ОШИБКА: doctor не вернул строку GATE — apply-hardcodes.mjs сломан или это не тот установщик.')
    process.exit(1)
  }
  return gate
}

function doctorShouldFail(gate) {
  return gate.crMissFile > 0
}

function writeDoctorStatus(gate, asInstall) {
  if (gate.crMissFile > 0) {
    if (asInstall) {
      console.log('ОШИБКА: doctor — пропал файл критичного правила реестра.')
      console.log('  Апстрим убрал kanban или connection-registry. Скачайте свежий релиз мода или обновите registry/overrides.')
    } else {
      console.log('статус: FAIL')
      console.log('  Пропал файл критичного правила (обычно kanban/plugin.tsx или connection-registry.ts).')
    }
    return
  }
  if (gate.crMiss > 0 || gate.crAmb > 0) {
    const n = gate.crMiss + gate.crAmb
    if (asInstall) {
      console.log(`ПРЕДУПРЕЖДЕНИЕ: ${n} критичных правил не применились — фичи мода, зависящие от них, будут отключены.`)
      console.log('  Установка продолжается (эти места останутся в поведении Hermes как в апстриме).')
    } else {
      console.log(`статус: WARN (установка возможна, ${n} критичных фич отключено)`)
    }
    return
  }
  if (asInstall) {
    console.log('doctor: критичные правила — все на месте')
    if (gate.cosMiss > 0 || gate.cosAmb > 0) {
      console.log(`ПРЕДУПРЕЖДЕНИЕ: косметика missing=${gate.cosMiss} ambiguous=${gate.cosAmb} (см. PROBLEMS) — затронутые места останутся на английском.`)
    }
  } else if (gate.cosMiss > 0 || gate.cosAmb > 0) {
    console.log(`статус: WARN (косметика missing=${gate.cosMiss} ambiguous=${gate.cosAmb} — эти места останутся на английском, установка идёт)`)
  } else {
    console.log('статус: OK (сухой прогон, ничего не записано)')
  }
}

function findAsarJs(root) {
  const candidates = [
    path.join(root, 'node_modules', '@electron', 'asar', 'bin', 'asar.js'),
    path.join(root, 'apps', 'desktop', 'node_modules', '@electron', 'asar', 'bin', 'asar.js'),
  ]
  for (const p of candidates) {
    if (existsSync(p)) return p
  }
  return null
}

function listWinProcesses() {
  const script = [
    'Get-Process -ErrorAction SilentlyContinue | ForEach-Object {',
    '  $p = $null',
    '  try { $p = $_.Path } catch { return }',
    '  if (-not $p) { return }',
    '  Write-Output ("{0}|{1}|{2}" -f $_.Id, $_.ProcessName, $p)',
    '}',
  ].join(' ')
  const r = run('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', script])
  if (r.error || r.status !== 0) return []
  const out = []
  for (const line of String(r.stdout || '').split(/\r?\n/)) {
    const parts = line.split('|')
    if (parts.length < 3) continue
    const pid = Number(parts[0])
    if (!Number.isFinite(pid)) continue
    out.push({ pid, name: parts[1], exe: parts.slice(2).join('|').trim() })
  }
  return out
}

function listPosixProcesses() {
  const r = run('ps', ['-ax', '-o', 'pid=,args='])
  if (r.error || r.status !== 0) return []
  const out = []
  for (const line of String(r.stdout || '').split(/\n/)) {
    const m = line.trim().match(/^(\d+)\s+(.*)$/)
    if (!m) continue
    out.push({ pid: Number(m[1]), name: '', exe: m[2] })
  }
  return out
}

function shouldSkipPid(pid, exe) {
  if (!pid || pid === process.pid || pid === process.ppid) return true
  if (pid <= 1) return true
  const s = String(exe || '').replace(/\\/g, '/').toLowerCase()
  if (s.includes('package/install.mjs') || s.includes('install.mjs')) return true
  if (s.includes('hermes-desktop-ru')) return true
  return false
}

function stopHermesRelated(cloneRoot, pack) {
  const roots = [cloneRoot, pack && pack.resources, pack && path.dirname(pack.resources)].filter(Boolean)
  const procs = isWin ? listWinProcesses() : listPosixProcesses()
  const killed = []
  for (const p of procs) {
    if (shouldSkipPid(p.pid, p.exe)) continue
    const hit = roots.some((root) => pathInside(p.exe, root) || String(p.exe).toLowerCase().replace(/\\/g, '/').includes(normPath(root)))
    if (!hit) continue
    try {
      if (isWin) {
        run('taskkill', ['/PID', String(p.pid), '/F', '/T'])
      } else {
        try {
          process.kill(p.pid, 'SIGTERM')
        } catch {
          /* already gone */
        }
      }
      killed.push(`${p.name || 'pid'}:${p.pid}`)
    } catch {
      /* ignore */
    }
  }
  if (!isWin && killed.length) {
    sleepSync(1500)
    for (const token of killed) {
      const pid = Number(String(token).split(':').pop())
      if (!pid) continue
      try {
        process.kill(pid, 0)
        process.kill(pid, 'SIGKILL')
      } catch {
        /* gone */
      }
    }
  }
  const uniq = [...new Set(killed)]
  if (uniq.length) {
    console.log(`остановлены процессы: ${uniq.join(', ')}`)
    sleepSync(2000)
  } else {
    console.log('процессы Hermes не найдены (ок)')
  }
}

function printRootHints() {
  console.error('ОШИБКА: не найден клон hermes-agent.')
  console.error('  Ожидается apps/desktop/package.json в одном из путей:')
  console.error('  - ~/.hermes/hermes-agent')
  console.error('  - %LOCALAPPDATA%\\hermes\\hermes-agent')
  console.error('  - $HERMES_AGENT_ROOT / $HERMES_INSTALL_DIR / $HERMES_HOME/hermes-agent')
  console.error('  Или: node install.mjs --root /path/to/hermes-agent')
}

function packHint() {
  if (isMac) return 'cd apps/desktop && npm run pack   # Hermes.app в release/mac-arm64 или release/mac'
  if (isLinux) return 'cd apps/desktop && npm run pack   # linux-unpacked в release/'
  return 'cd apps/desktop && npm run pack   # win-unpacked в release/'
}

function codesignIfMac(pack) {
  if (!isMac || !pack) return
  let app = pack.resources
  for (let i = 0; i < 4; i++) {
    if (app.toLowerCase().endsWith('.app')) break
    app = path.dirname(app)
  }
  if (!app.toLowerCase().endsWith('.app') || !existsSync(app)) {
    console.log('ПРЕДУПРЕЖДЕНИЕ: не нашёл Hermes.app рядом с asar — codesign пропущен')
    return
  }
  const xattr = run('xattr', ['-cr', app])
  if (xattr.error) {
    console.log(`ПРЕДУПРЕЖДЕНИЕ: xattr недоступен (${xattr.error.message})`)
  }
  const sign = run('codesign', ['--force', '--sign', '-', '--deep', app])
  if (sign.error) {
    console.log(`ПРЕДУПРЕЖДЕНИЕ: codesign недоступен (${sign.error.message}) — Gatekeeper может не пустить приложение`)
    return
  }
  if (sign.status !== 0) {
    console.log(`ПРЕДУПРЕЖДЕНИЕ: ad-hoc codesign не удался (exit ${sign.status}).`)
    if (sign.stderr) process.stdout.write(sign.stderr)
    console.log('  Это self-built .app из клона; официальный notarized бинарник с сайта мы не патчим.')
    return
  }
  console.log('codesign: ad-hoc подпись обновлена (self-built .app)')
}

function ensureDir(p) {
  mkdirSync(p, { recursive: true })
}

function selfTest() {
  const failures = []
  const ver = readVersion()
  if (!ver) failures.push('version empty')

  const a = parseArgs(['doctor', '--root', '/tmp/x'])
  if (a.cmd !== 'doctor' || a.root !== '/tmp/x') failures.push('parseArgs doctor --root')
  const b = parseArgs(['install', '-Root', 'D:\\foo'])
  if (b.cmd !== 'install' || b.root !== 'D:\\foo') failures.push('parseArgs -Root')
  const c = parseArgs(['--self-test'])
  if (c.cmd !== 'self-test') failures.push('parseArgs --self-test')
  const d = parseArgs(['install', '--allow-stale-dist'])
  if (!d.allowStaleDist) failures.push('parseArgs --allow-stale-dist')

  const tmp = mkdtempSync(path.join(tmpdir(), 'hdru-self-'))
  try {
    const clone = path.join(tmp, 'hermes-agent')
    const linuxRes = path.join(clone, 'apps', 'desktop', 'release', 'linux-unpacked', 'resources')
    const winRes = path.join(clone, 'apps', 'desktop', 'release', 'win-unpacked', 'resources')
    const macRes = path.join(clone, 'apps', 'desktop', 'release', 'mac-arm64', 'Hermes.app', 'Contents', 'Resources')
    ensureDir(linuxRes)
    ensureDir(winRes)
    ensureDir(macRes)
    writeFileSync(path.join(clone, 'apps', 'desktop', 'package.json'), '{"name":"hermes"}\n')
    writeFileSync(path.join(linuxRes, 'app.asar'), 'linux')
    writeFileSync(path.join(winRes, 'app.asar'), 'win')
    writeFileSync(path.join(macRes, 'app.asar'), 'mac')

    if (!isHermesClone(clone)) failures.push('isHermesClone fake tree')
    if (isHermesClone(tmp)) failures.push('isHermesClone false positive')

    const pack = resolvePack(clone)
    if (!pack || !existsSync(pack.asar)) failures.push('resolvePack missing')
    if (pack && !pathInside(pack.asar, path.join(clone, 'apps', 'desktop', 'release'))) {
      failures.push('resolvePack escaped release/')
    }

    const outside = path.join(tmp, 'Applications', 'Hermes.app', 'Contents', 'Resources')
    ensureDir(outside)
    writeFileSync(path.join(outside, 'app.asar'), 'official')
    const pack2 = resolvePack(clone)
    if (pack2 && pathInside(pack2.asar, path.join(tmp, 'Applications'))) {
      failures.push('resolvePack picked /Applications')
    }

    const cands = rootCandidates(clone)
    if (!cands.some((p) => normPath(p) === normPath(clone))) failures.push('rootCandidates explicit')

    const applyJs = path.join(here, 'apply-hardcodes.mjs')
    if (!existsSync(applyJs)) {
      console.log('self-test: apply-hardcodes.mjs отсутствует в этой раскладке (ок для урезанного zip)')
    }
  } finally {
    rmSync(tmp, { recursive: true, force: true })
  }

  if (failures.length) {
    console.error('self-test FAIL')
    for (const f of failures) console.error(`  - ${f}`)
    process.exit(1)
  }
  console.log(`self-test OK  (install.mjs v${ver}, platform=${process.platform} arch=${process.arch})`)
  process.exit(0)
}

function cmdDoctor(root) {
  const registry = path.join(here, 'registry.json')
  const expectFile = path.join(here, 'EXPECTED_COMMIT')
  if (!existsSync(registry)) {
    console.error('ОШИБКА: registry.json не найден рядом с установщиком')
    process.exit(1)
  }
  const st = runGit(root, ['status', '--porcelain', '--untracked-files=no'])
  if (!st.error && st.status === 0 && String(st.stdout || '').trim()) {
    console.log('ПРЕДУПРЕЖДЕНИЕ: в клоне есть локальные правки tracked-файлов.')
    console.log('  Doctor проверяет ТЕКУЩЕЕ дерево и ничего не откатывает.')
    console.log('  Для проверки против стока сначала: git restore --source=HEAD --staged --worktree .')
  }
  const actual = showVersionGate(root, expectFile)
  const gate = invokeDoctor(root, registry)
  console.log('')
  console.log('=== ОТЧЁТ DOCTOR ===')
  console.log(`HEAD клона : ${actual}`)
  console.log(`реестр     : ${registry}`)
  writeDoctorStatus(gate, false)
  process.exit(doctorShouldFail(gate) ? 1 : 0)
}

function cmdUninstall(root) {
  const pack = resolvePack(root)
  if (!pack) {
    console.error('ОШИБКА: не найден packaged app.asar в клоне.')
    console.error(`  Искал под ${path.join(root, 'apps', 'desktop', 'release')}`)
    console.error(`  ${packHint()}`)
    process.exit(1)
  }
  stopHermesRelated(root, pack)
  const bak = `${pack.asar}.stock.bak`
  if (!existsSync(bak)) {
    console.error('ОШИБКА: нет app.asar.stock.bak — нечего откатывать.')
    console.error(`  Ожидался файл: ${bak}`)
    console.error('  Его создаёт install при первой установке. Полный сброс — hermes update.')
    process.exit(1)
  }
  copyFileSync(bak, pack.asar)
  console.log('app.asar восстановлен из .stock.bak')
  const distBak = path.join(pack.unpacked, 'dist.stock.bak')
  const distLive = path.join(pack.unpacked, 'dist')
  if (existsSync(distBak)) {
    if (existsSync(distLive)) rmSync(distLive, { recursive: true, force: true })
    cpSync(distBak, distLive, { recursive: true })
    console.log('app.asar.unpacked/dist восстановлен из dist.stock.bak')
  }
  codesignIfMac(pack)
  console.log('ОТКАТ OK — packaged Desktop снова стоковый.')
  console.log('  Исходники клона не трогались. Полный сброс клона — hermes update.')
  process.exit(0)
}

function ensureDeps(root) {
  const health = path.join(here, 'deps-health.mjs')
  if (!existsSync(health)) {
    console.log('ПРЕДУПРЕЖДЕНИЕ: deps-health.mjs нет — пропускаю проверку зависимостей')
    return
  }
  let r = run(process.execPath, [health, root], { cwd: root, stdio: 'inherit' })
  if (!r.error && r.status === 0) {
    console.log('зависимости: OK')
    return
  }
  const lock = existsSync(path.join(root, 'package-lock.json'))
  if (lock) {
    console.log('зависимости повреждены — npm ci (3–10 мин)...')
    r = runNpm(['ci'], root, true)
  } else {
    console.log('зависимости повреждены — npm install...')
    r = runNpm(['install'], root, true)
  }
  if (r.error) {
    console.error(`ОШИБКА: npm недоступен (${r.error.message})`)
    process.exit(1)
  }
  r = run(process.execPath, [health, root], { cwd: root, stdio: 'inherit' })
  if (r.error || r.status !== 0) {
    console.error('ОШИБКА: после переустановки node_modules пакеты всё ещё отсутствуют (проверьте сеть/npm)')
    process.exit(1)
  }
  console.log('зависимости восстановлены')
}

function cmdInstall(root, allowStaleDist) {
  const registry = path.join(here, 'registry.json')
  const expectFile = path.join(here, 'EXPECTED_COMMIT')
  const desktop = path.join(root, 'apps', 'desktop')
  const modDist = path.join(here, 'dist')
  if (!existsSync(registry)) {
    console.error('ОШИБКА: registry.json не найден рядом с установщиком')
    process.exit(1)
  }

  ensureDeps(root)
  const asarJs = findAsarJs(root)
  if (!asarJs) {
    console.error('ОШИБКА: @electron/asar не найден после шага зависимостей')
    process.exit(1)
  }

  const packEarly = resolvePack(root)
  stopHermesRelated(root, packEarly)
  showVersionGate(root, expectFile)

  const restore = runGit(root, ['restore', '--source=HEAD', '--staged', '--worktree', '.'])
  const restoreExit = restore.error ? 1 : restore.status
  console.log(`сброс к стоку: exit=${restoreExit} (untracked-локали не трогаем)`)

  const gate = invokeDoctor(root, registry)
  if (doctorShouldFail(gate)) {
    writeDoctorStatus(gate, true)
    process.exit(1)
  }
  writeDoctorStatus(gate, true)

  const applyJs = path.join(here, 'apply-hardcodes.mjs')
  const apply = run(process.execPath, [applyJs, root, registry], { cwd: root, stdio: 'inherit' })
  if (apply.error || apply.status !== 0) {
    console.error('ОШИБКА: apply реестра прерван (пропал файл критичного правила)')
    process.exit(1)
  }
  console.log('apply: реестр применён (косметические пропуски, если были, оставлены как есть)')

  const fileMap = [
    ['files/ru.ts', path.join('apps', 'desktop', 'src', 'i18n', 'ru.ts')],
    ['files/ru-constants.ts', path.join('apps', 'desktop', 'src', 'app', 'settings', 'ru-constants.ts')],
    ['files/ru-locales.ts', path.join('apps', 'desktop', 'src', 'plugins', 'kanban', 'ru-locales.ts')],
  ]
  let copied = 0
  for (const [srcRel, dstRel] of fileMap) {
    const src = resolveModFile(srcRel)
    const dst = path.join(root, dstRel)
    if (src) {
      ensureDir(path.dirname(dst))
      copyFileSync(src, dst)
      console.log(`локаль: ${dstRel.replace(/\\/g, '/')}`)
      copied++
    } else {
      console.log(`ПРЕДУПРЕЖДЕНИЕ: не найден файл мода ${srcRel} (и плоский fallback)`)
    }
  }
  if (copied < 1) {
    console.error('ОШИБКА: ни один locale-файл мода не найден рядом с установщиком')
    process.exit(1)
  }

  const pack = resolvePack(root)
  if (pack) {
    if (existsSync(pack.asar) && !existsSync(`${pack.asar}.stock.bak`)) {
      copyFileSync(pack.asar, `${pack.asar}.stock.bak`)
    }
    const liveDist = path.join(pack.unpacked, 'dist')
    const distBak = path.join(pack.unpacked, 'dist.stock.bak')
    if (existsSync(liveDist) && !existsSync(distBak)) {
      cpSync(liveDist, distBak, { recursive: true })
    }
    console.log('бэкапы: OK')
  } else {
    console.log('бэкапы: пропуск (packaged asar ещё не найден — проверим после сборки)')
  }

  const i18nDir = path.join(root, 'apps', 'desktop', 'src', 'i18n')
  const struct = path.join(here, 'structural-i18n.mjs')
  if (existsSync(struct)) {
    const s = run(process.execPath, [struct, i18nDir], { cwd: root, stdio: 'inherit' })
    if (s.error || s.status !== 0) {
      console.error('ОШИБКА: structural-i18n')
      process.exit(1)
    }
    console.log('регистрация ru: OK')
  } else {
    console.log('ПРЕДУПРЕЖДЕНИЕ: structural-i18n.mjs отсутствует — язык ru может не попасть в бандл')
  }

  console.log('сборка dist (npm run build, 5–10 мин)...')
  const buildLog = path.join(tmpdir(), 'mod-build.log')
  let fd
  try {
    fd = openSync(buildLog, 'w')
    const b = spawnSync(isWin ? 'npm.cmd' : 'npm', ['run', 'build'], {
      cwd: desktop,
      stdio: ['ignore', fd, fd],
      windowsHide: true,
      shell: isWin,
    })
    closeSync(fd)
    fd = null
    let usePackage = false
    if (b.error || b.status !== 0) {
      console.error(`ОШИБКА: npm run build failed (exit ${b.error ? b.error.message : b.status}) — см. ${buildLog}`)
      if (allowStaleDist && existsSync(path.join(modDist, 'index.html'))) {
        console.log('ПРЕДУПРЕЖДЕНИЕ: --allow-stale-dist — беру package/dist (может не совпасть с этим апстримом)')
        usePackage = true
      } else {
        console.error('  Повтор с устаревшим package/dist отключён (иначе «УСТАНОВКА OK» со старым UI).')
        console.error('  Если очень надо: node install.mjs --allow-stale-dist')
        process.exit(1)
      }
    } else {
      console.log('сборка: OK')
    }

    const packNow = resolvePack(root)
    if (!packNow) {
      console.error('ОШИБКА: не найден packaged app.asar.')
      console.error(`  Искал под ${path.join(root, 'apps', 'desktop', 'release')}`)
      console.error('  Сначала соберите Desktop из клона (не prebuilt с сайта):')
      console.error(`  ${packHint()}`)
      process.exit(1)
    }

    const list = run(process.execPath, [asarJs, 'list', '-i', packNow.asar], { cwd: root })
    const unpackedFiles = []
    for (const line of String(list.stdout || '').split(/\r?\n/)) {
      const m = line.match(/^unpack\s*:\s*(.+)$/)
      if (m) unpackedFiles.push(m[1].trim().replace(/^[\\/]+/, ''))
    }
    console.log(`unpack-marked: ${unpackedFiles.length}`)
    for (const f of unpackedFiles) {
      const dest = path.join(packNow.unpacked, f)
      ensureDir(path.dirname(dest))
      if (!existsSync(dest)) writeFileSync(dest, '')
    }

    const tmp = mkdtempSync(path.join(tmpdir(), 'asar-mod-'))
    const app = path.join(tmp, 'app')
    try {
      ensureDir(app)
      const ext = run(process.execPath, [asarJs, 'extract', packNow.asar, app], { cwd: root, stdio: 'inherit' })
      if (ext.error || ext.status !== 0) {
        console.error('ОШИБКА: extract asar')
        process.exit(1)
      }
      const srcDist = usePackage ? modDist : path.join(desktop, 'dist')
      const appDist = path.join(app, 'dist')
      if (existsSync(appDist)) rmSync(appDist, { recursive: true, force: true })
      cpSync(srcDist, appDist, { recursive: true })
      console.log(`dist из: ${usePackage ? 'package (stale, --allow-stale-dist)' : 'clone build'}`)

      if (existsSync(packNow.unpacked)) rmSync(packNow.unpacked, { recursive: true, force: true })
      const pk = run(process.execPath, [asarJs, 'pack', app, packNow.asar, '--unpack', '**'], {
        cwd: root,
        stdio: 'inherit',
      })
      if (pk.error || pk.status !== 0) {
        console.error('ОШИБКА: pack asar')
        process.exit(1)
      }
    } finally {
      rmSync(tmp, { recursive: true, force: true })
    }

    codesignIfMac(packNow)

    const probeJs = path.join(here, 'probe-ru.mjs')
    const physIndex = existsSync(path.join(packNow.unpacked, 'dist', 'index.html'))
    const physMain = existsSync(path.join(packNow.unpacked, 'dist', 'electron-main.mjs'))
    const physPkg = existsSync(path.join(packNow.unpacked, 'package.json'))
    let ruMarker = 'нет'
    const assetsDir = path.join(packNow.unpacked, 'dist', 'assets')
    if (existsSync(assetsDir) && existsSync(probeJs)) {
      const ru = run(process.execPath, [probeJs, assetsDir])
      const token = String(ru.stdout || '').trim()
      if (token && token !== 'NONE') ruMarker = `FOUND (${token})`
    } else if (!existsSync(probeJs)) {
      console.log('ПРЕДУПРЕЖДЕНИЕ: probe-ru.mjs отсутствует — пропускаю проверку маркера')
    }
    console.log(`проверки: index=${physIndex} main=${physMain} pkg=${physPkg} ru=${ruMarker}`)
    if (!(physIndex && physMain && physPkg)) {
      console.error('ОШИБКА: проверки упаковки провалены — восстановите app.asar.stock.bak')
      process.exit(1)
    }
    if (ruMarker === 'нет') {
      console.log('ПРЕДУПРЕЖДЕНИЕ: RU-маркер не найден — мод мог не попасть в бандл')
    }
    console.log('УСТАНОВКА OK — перезапустите Hermes Desktop')
    if (!isWin) {
      console.log('  Linux/macOS: экспериментально. Если Desktop не открывается — это self-built')
      console.log('  из клона; официальный бинарник с сайта мод не патчит.')
    }
  } finally {
    if (fd != null) {
      try {
        closeSync(fd)
      } catch {
        /* ignore */
      }
    }
  }
}

function main(argv = process.argv.slice(2)) {
  const args = parseArgs(argv)
  if (args.cmd === 'help') {
    showHelp()
    process.exit(0)
  }
  if (args.cmd === 'version') {
    console.log(readVersion())
    process.exit(0)
  }
  if (args.cmd === 'self-test') {
    selfTest()
    return
  }

  const modVer = readVersion()
  if (args.cmd !== 'install' && args.cmd !== 'doctor' && args.cmd !== 'uninstall') {
    console.error(`Неизвестная команда: ${args.cmd}`)
    process.exit(2)
  }

  const root = resolveHermesRoot(args.root)
  if (!root) {
    printRootHints()
    process.exit(1)
  }

  console.log(`== Hermes Desktop RU — установщик v${modVer} ==`)
  console.log(`клон: ${root}`)
  console.log(`платформа: ${process.platform}/${process.arch}${isWin ? '' : ' (POSIX — экспериментально)'}`)

  if (args.cmd === 'doctor') cmdDoctor(root)
  else if (args.cmd === 'uninstall') cmdUninstall(root)
  else cmdInstall(root, args.allowStaleDist)
}

const launchedAsMain = (() => {
  const entry = process.argv[1] && path.resolve(process.argv[1])
  return entry && path.resolve(fileURLToPath(import.meta.url)) === entry
})()

if (launchedAsMain) {
  main()
}

export {
  parseArgs,
  isHermesClone,
  resolveHermesRoot,
  resolvePack,
  readVersion,
  rootCandidates,
}