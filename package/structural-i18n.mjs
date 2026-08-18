#!/usr/bin/env node
// structural-i18n.mjs — регистрация ru-локали в i18n-файлах Hermes Desktop.
// Структурные якоря (а не хунки патча): работают на любой версии/наборе локалей
// upstream, идемпотентно. Якорь не найден -> выброс (НИЧЕГО не пишем).
// EOL-сохраняющий, только node core.
// Наш патчер базируется на идее "структурных якорей" из @anatolijlaptev1991/hermes-ru.
import fs from 'node:fs'
import path from 'node:path'

const I18N_DIR = process.argv[2]

function PatchAnchorError(file, what) {
  const e = new Error(`[structural-i18n] ${file}: anchor not found → ${what}. Файл изменён апстримом или уже не в ожидаемой форме.`)
  e.code = 'ANCHOR'
  return e
}

function readUtf8(p) {
  const buf = fs.readFileSync(p)
  const eol = buf.includes(Buffer.from('\r\n')) ? '\r\n' : '\n'
  return { content: buf.toString('utf8'), eol }
}

function insertBeforeClose(content, closeIndex, insertLines, file, anchorName) {
  const before = content.slice(0, closeIndex)
  const after = content.slice(closeIndex)
  const trimmedEnd = before.replace(/\s+$/, '')
  if (!trimmedEnd) throw PatchAnchorError(file, `${anchorName} (пустой блок)`)
  const lastChar = trimmedEnd[trimmedEnd.length - 1]
  const comma = lastChar !== '{' && lastChar !== '[' && lastChar !== ',' ? ',' : ''
  return trimmedEnd + comma + '\n' + insertLines + after
}

// ---------- types.ts: Locale = 'en' | ... | 'ru' ----------
function patchTypes(content, file) {
  if (/export type Locale\s*=[^;\n]*'ru'/.test(content)) return { content, changed: false }
  const m = content.match(/^(export type Locale\s*=\s*)([^\n;]+?)([ \t]*)$/m)
  if (!m) throw PatchAnchorError(file, 'export type Locale = …')
  if (!/'[a-z-]+'/.test(m[2])) throw PatchAnchorError(file, 'члены Locale-union')
  return { content: content.replace(m[0], `${m[1]}${m[2]} | 'ru'${m[3]}`), changed: true }
}

// ---------- catalog.ts: import { ru } + TRANSLATIONS.ru ----------
function patchCatalog(content, file) {
  let out = content
  let changed = false

  if (!/from\s*'\.\/ru'/.test(out)) {
    const importRe = /^import\s+(?:type\s+)?\{\s*[\w,\s]*\w\s*\}\s*from\s*'(\.\/[\w-]+)'\s*;?\s*$/gm
    const imports = []
    let m
    while ((m = importRe.exec(out)) !== null) imports.push({ index: m.index, text: m[0], p: m[1] })
    if (!imports.length) throw PatchAnchorError(file, "import { … } from './<locale>'")
    const greater = imports.find(im => im.p > './ru')
    if (greater) {
      out = out.slice(0, greater.index) + "import { ru } from './ru'\n" + out.slice(greater.index)
    } else {
      const last = imports[imports.length - 1]
      out = out.slice(0, last.index + last.text.length) + "\nimport { ru } from './ru'" + out.slice(last.index + last.text.length)
    }
    changed = true
  }

  const tStart = out.search(/export const TRANSLATIONS[^[{]*\{/)
  if (tStart < 0) throw PatchAnchorError(file, 'export const TRANSLATIONS … {')
  const blockEnd = out.indexOf('\n}', tStart)
  if (blockEnd < 0) throw PatchAnchorError(file, 'закрывающая } TRANSLATIONS')
  const block = out.slice(tStart, blockEnd)
  if (!/(?:^|[,{\s])ru(?:\s*,|\s*$)/m.test(block)) {
    out = insertBeforeClose(out, blockEnd, '  ru', file, 'тело TRANSLATIONS')
    changed = true
  }
  return { content: out, changed }
}

// ---------- languages.ts: LOCALE_OPTIONS + LOCALE_ALIASES ----------
function patchLanguages(content, file) {
  let out = content
  let changed = false
  const eol = out.includes('\r\n') ? '\r\n' : '\n'

  if (!/id:\s*'ru'/.test(out)) {
    const asConst = out.search(/\]\s*as const/)
    if (asConst < 0) throw PatchAnchorError(file, '] as const (LOCALE_OPTIONS)')
    if ((out.match(/\]\s*as const/g) || []).length !== 1) throw PatchAnchorError(file, '] as const не уникален')
    const option = "  {" + eol + "    id: 'ru'," + eol + "    name: 'Русский'," + eol + "    englishName: 'Russian'," + eol + "    configValue: 'ru'" + eol + "  }"
    out = insertBeforeClose(out, asConst, option, file, 'LOCALE_OPTIONS')
    changed = true
  }

  if (!/^\s*ru:\s*'ru'/m.test(out)) {
    const aStart = out.search(/LOCALE_ALIASES[^[{]*\{/)
    if (aStart < 0) throw PatchAnchorError(file, 'LOCALE_ALIASES … {')
    const aEnd = out.indexOf('\n}', aStart)
    if (aEnd < 0) throw PatchAnchorError(file, 'закрывающая } LOCALE_ALIASES')
    const aliases = "  ru: 'ru'," + eol + "  'ru-ru': 'ru'," + eol + "  ru_ru: 'ru'," + eol + "  russian: 'ru'," + eol + "  русский: 'ru'"
    out = insertBeforeClose(out, aEnd, aliases, file, 'тело LOCALE_ALIASES')
    changed = true
  }
  return { content: out, changed }
}

const PATCHERS = {
  'types.ts': patchTypes,
  'catalog.ts': patchCatalog,
  'languages.ts': patchLanguages,
}

const results = []
for (const [file, fn] of Object.entries(PATCHERS)) {
  const p = path.join(I18N_DIR, file)
  if (!fs.existsSync(p)) throw new Error(`[structural-i18n] ${p} не найден — указан ли правильный src/i18n/ каталог?`)
  const { content, eol } = readUtf8(p)
  const r = fn(content.endsWith('\n') ? content : content + '\n', file)
  if (r.changed) {
    fs.writeFileSync(p, r.content.replace(/\n/g, eol))
    results.push(`patched: ${file}`)
  } else {
    results.push(`ok (already ru): ${file}`)
  }
}
console.log('[structural-i18n] ' + results.join(' | '))
