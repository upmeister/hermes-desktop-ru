#!/usr/bin/env node
// hermes-desktop-ru CLI — тонкая обёртка над package/install.mjs
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const here = path.dirname(fileURLToPath(import.meta.url))
const installer = path.join(here, '..', 'package', 'install.mjs')
const pkgPath = path.join(here, '..', 'package.json')

function readVersion() {
  try {
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'))
    return pkg.version || 'unknown'
  } catch {
    return 'unknown'
  }
}

function printHelp() {
  console.log('hermes-desktop-ru — русская локализация Hermes Desktop')
  console.log('')
  console.log('  hermes-desktop-ru install              установить / переустановить мод')
  console.log('  hermes-desktop-ru doctor               сухая проверка совместимости')
  console.log('  hermes-desktop-ru uninstall            откатить app.asar из .stock.bak')
  console.log('  hermes-desktop-ru version              версия пакета (из package.json)')
  console.log('  hermes-desktop-ru help                 справка')
  console.log('')
  console.log('Флаги install: --root <путь к клону hermes-agent>, --allow-stale-dist')
  console.log('Клон: --root · HERMES_AGENT_ROOT · HERMES_INSTALL_DIR · $HERMES_HOME/hermes-agent')
  console.log('      ~/.hermes/hermes-agent · /usr/local/lib/hermes-agent · %LOCALAPPDATA%\\hermes\\hermes-agent')
  console.log('Linux: установщик прогнан автором. После install — hermes desktop --skip-build.')
  console.log('macOS — экспериментально (автор на живой машине не гонял).')
}

const args = process.argv.slice(2)
if (args.length === 0) {
  printHelp()
  process.exit(0)
}

const cmd = args[0]
if (cmd === 'version' || cmd === '--version' || cmd === '-v') {
  console.log(readVersion())
  process.exit(0)
}
if (cmd === 'help' || cmd === '--help' || cmd === '-h') {
  printHelp()
  process.exit(0)
}

const r = spawnSync(process.execPath, [installer, ...args], {
  stdio: 'inherit',
})

if (r.error) {
  console.error(`Не удалось запустить установщик: ${r.error.message}`)
  console.error('Нужен Node.js 18+.')
  process.exit(1)
}

process.exit(r.status ?? 1)