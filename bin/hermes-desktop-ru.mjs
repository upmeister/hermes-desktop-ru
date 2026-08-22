#!/usr/bin/env node
// hermes-desktop-ru CLI — тонкая обёртка над PowerShell-установщиком.
// npm кладёт этот скрипт в PATH (shim), установщик лежит рядом: ../package/install-asar.ps1
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const here = path.dirname(fileURLToPath(import.meta.url))
const installer = path.join(here, '..', 'package', 'install-asar.ps1')
const pkgPath = path.join(here, '..', 'package.json')

function readVersion() {
  try {
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'))
    return pkg.version || 'unknown'
  } catch {
    return 'unknown'
  }
}

const [, , cmd, ...rest] = process.argv

function printHelp() {
  console.log('hermes-desktop-ru — русская локализация Hermes Desktop')
  console.log('')
  console.log('  hermes-desktop-ru install              установить / переустановить мод')
  console.log('  hermes-desktop-ru doctor               сухая проверка совместимости')
  console.log('  hermes-desktop-ru uninstall            откатить app.asar из .stock.bak')
  console.log('  hermes-desktop-ru version              версия пакета (из package.json)')
  console.log('  hermes-desktop-ru help                 справка')
  console.log('')
  console.log('Флаги install: -Root <путь к клону hermes-agent>, -AllowStaleDist')
}

let psArgs
switch (cmd) {
  case 'install':
    psArgs = rest
    break
  case 'doctor':
    psArgs = ['-Doctor', ...rest]
    break
  case 'uninstall':
    psArgs = ['-Uninstall', ...rest]
    break
  case 'version':
  case '--version':
  case '-v':
    console.log(readVersion())
    process.exit(0)
  case 'help':
  case '--help':
  case '-h':
    psArgs = ['-Help']
    break
  case undefined:
    printHelp()
    process.exit(0)
  default:
    console.error(`Неизвестная команда: ${cmd}. Доступно: install, doctor, uninstall, version, help`)
    process.exit(2)
}

const r = spawnSync('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', installer, ...psArgs], {
  stdio: 'inherit'
})

if (r.error) {
  console.error(`Не удалось запустить PowerShell: ${r.error.message}`)
  console.error('CLI работает на Windows; на других ОС используйте install-asar.ps1 напрямую.')
  process.exit(1)
}

process.exit(r.status ?? 1)