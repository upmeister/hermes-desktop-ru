// Измерение покрытия core-локалей через реалемп (без regex-артефактов).
// node measure-locales.mjs <repoRoot>/apps/desktop/src/i18n
import fs from 'node:fs'
import path from 'node:path'

// Разбор одного файла: filePath + имя константы (обычно = локаль, но в
// plugins/<name>/i18n.ts лежат en/ja/zh/zhHant рядом, а в мод-файлах — ru).
// CLI: node measure-locales.mjs <dir> [--pairs "en:file1,ru:file2"] [локали...]
const dir = process.argv[2]
if (!dir || !fs.existsSync(dir)) { console.error('usage: node measure-locales.mjs <i18nDir> [locales...]'); process.exit(2) }

// Вырезать тело локали. Формы в апстриме разные:
//   en.ts : export const en: Translations = { ... }
//   ru.ts : export const ru = defineLocale({ ... })
//   de.ts : export const de = defineLocale({ base: en, overrides: { ... } })
// Поэтому ищем `const <name>` и берём ПЕРВУЮ парную `{` после `=`,
// а для override-локалей дополнительно вырезаем `overrides`.
function body(src, name) {
  const m = new RegExp(`\\bconst\\s+${name}\\b[^=]*=`, 'm').exec(src)
  if (!m) return null
  // ru: первый объект после '=' — сам каталог.
  const eq = src.indexOf('=', m.index + m[0].length - 1)
  const brace = src.indexOf('{', eq)
  if (brace === -1) return null
  let depth = 0, i = brace, q = null
  for (; i < src.length; i++) {
    const c = src[i]
    if (q) {
      if (c === '\\') { i++; continue }
      if (c === q) q = null
      continue
    }
    if (c === "'" || c === '"' || c === '`') { q = c; continue }
    if (c === '/' && src[i + 1] === '/') { while (i < src.length && src[i] !== '\n') i++; continue }
    if (c === '/' && src[i + 1] === '*') { i += 2; while (i < src.length && !(src[i] === '*' && src[i + 1] === '/')) i++; i++; continue }
    if (c === '{') depth++
    else if (c === '}') { depth--; if (depth === 0) break }
  }
  const outer = src.slice(brace, i + 1)
  // Если каталог обёрнут в base/overrides — берём только overrides.
  const om = /\boverrides\s*:\s*\{/.exec(outer)
  if (om && !/^\{\s*$/.test(outer.trim().slice(0, 200))) {
    const ob = outer.indexOf('{', om.index + om[0].length - 1)
    let d2 = 0, j = ob, q2 = null
    for (; j < outer.length; j++) {
      const c = outer[j]
      if (q2) {
        if (c === '\\') { j++; continue }
        if (c === q2) q2 = null
        continue
      }
      if (c === "'" || c === '"' || c === '`') { q2 = c; continue }
      if (c === '{') d2++
      else if (c === '}') { d2--; if (d2 === 0) break }
    }
    return outer.slice(ob, j + 1)
  }
  return outer
}

// Снять TS-хвосты: аннотации в стрелках + операторы `as` / `satisfies`.
// ВАЖНО: `as` снимается ТОЛЬКО как отдельное слово (`} as X`), иначе регулярка
// съедает обычный текст внутри строк ('Nothing here reads as a server').
// Поэтому сначала режем ТОЛЬКО известные TS-формы, а не слово `as` подряд.
function stripTypes(b) {
  let s = b
  // `} as Record<...>`, `as const` — якорь на закрывающую скобку/выражение.
  for (let pass = 0; pass < 4; pass++) {
    const before = s
    s = s.replace(/([}\)\]])(\s+)as\s+(const\b|[A-Za-z_$][\w$]*(?:<[^<>]*>)?)/g, '$1')
    s = s.replace(/([}\)\]])\s+satisfies\s+[A-Za-z_$][\w$<>\[\]|&., ]*?(?=[,;)\]}])/g, '$1')
    if (s === before) break
  }
  // Аннотации в стрелках. Три формы, все встречаются в апстриме:
  //   (app: string) => …   — скобочная с типами (двоеточие ВНУТРИ скобок)
  //   (a: number, b: string) => … — несколько параметров
  //   term => …            — бескобочная (в ru.ts таких много)
  // Бескобочная форма ломает реалемп: `tryHint => …` как свойство объекта
  // требует скобок. Параметр подставляем УНИКАЛЬНЫМ и заведомо не
  // зарезервированным (`__a0`), иначе `delete: (delete) =>` роняет парсер.
  let argN = 0
  for (let pass = 0; pass < 4; pass++) {
    const before = s
    // скобочная с типами: убираем `имя: Тип` ВНУТРИ скобок, оставляя `имя`.
    // Терминатор типа: запятая, закрывающая скобка ИЛИ конец строки —
    // внутри `(name: string)` закрывающей скобки нет, тип оканчивается EOL.
    s = s.replace(/\(([^()]*)\)/g, (m, inner) => {
      const cleaned = inner.replace(/([A-Za-z_$][\w$]*)\s*:\s*[A-Za-z_$][\w$<>\[\]|&. ]*?(\s*[,)]|$)/g, '$1$2')
      return '(' + cleaned + ')'
    })
    // бескобочный параметр с типом: `term: T =>` → `term =>`
    s = s.replace(/([A-Za-z_$][\w$]*)\s*:\s*[A-Za-z_$][\w$<>\[\]|&. ]*?(?=\s*=>)/g, '$1')
    // бескобочный параметр как свойство: `tryHint =>` → `tryHint: (__a0) =>`
    s = s.replace(/^(\s*)([A-Za-z_$][\w$]*)\s*=>/gm, (m, ind, name) => {
      const a = '__a' + (argN++)
      return ind + name + ': (' + a + ') =>'
    })
    if (s === before) break
  }
  return s
}

// Реалемп в песочнице: пути + isFn + арность.
// Локали НЕ самодостаточны: en.ts тянет FIELD_LABELS/FIELD_DESCRIPTIONS из
// @/app/settings/constants, ru.ts зовёт defineFieldCopy. Поэтому в песочницу
// подставляются заглушки — иначе тело локали не парсится как JS.
// Тело оборачивается в IIFE с export default: верхнеуровневый `return`
// в ES-модуле запрещён («Illegal return statement»).
async function flatten(src, prelude = '') {
  const body = `
    const __obj = ${src};
    const __out = {};
    (function walk(o, p) {
      for (const k of Object.keys(o)) {
        const v = o[k], np = p ? p + '.' + k : k;
        if (v && typeof v === 'function') __out[np] = { fn: true, arity: v.length };
        else if (v && typeof v === 'object' && !Array.isArray(v)) { __out[np] = { obj: true }; walk(v, np); }
        else __out[np] = { fn: false, val: v };
      }
    })(__obj, '');
    return __out;
  `
  const code = prelude + '\nconst __run = () => {\n' + body + '\n};\nexport default __run();\n'
  const mod = await import('data:text/javascript;base64,' + Buffer.from(code, 'utf8').toString('base64'))
  return mod.default
}

// Заглушки для внешних символов, на которые ссылается тело локали.
const PRELUDE = `
const __EMPTY = {};
const FIELD_LABELS = __EMPTY;
const FIELD_DESCRIPTIONS = __EMPTY;
const defineFieldCopy = (x) => x;
const defineLocale = (x) => x;
`

const names = process.argv.slice(3)
const results = {}

for (const loc of names) {
  // Формы размещения: src/i18n/<loc>.ts (ядро) ИЛИ plugins/<name>/i18n.ts (плагин,
  // где все локали живут в одном файле — тогда берём его за <loc>.ts).
  let file = path.join(dir, `${loc}.ts`)
  if (!fs.existsSync(file)) {
    const bundle = path.join(dir, 'i18n.ts')
    if (fs.existsSync(bundle)) file = bundle
  }
  if (!fs.existsSync(file)) { results[loc] = { error: 'нет файла' }; continue }
  const raw = fs.readFileSync(file, 'utf8')
  const b = body(raw, loc)
  if (!b) { results[loc] = { error: 'не найден const ' + loc }; continue }
  try {
    const flat = await flatten(stripTypes(b), PRELUDE)
    results[loc] = { keys: Object.keys(flat).length, flat }
  } catch (e) {
    results[loc] = { error: e.message }
  }
}

// Сравнение целевой локали против базовой (первой в argv, не ru).
// Скрипт НЕ зашит на ru: `node measure-locales.mjs <dir> en ru|fr|de|es|ja|zh`.
const base = names[0]
const target = names[1]
if (!base || !target || !results[base]?.flat || !results[target]?.flat) {
  console.log(JSON.stringify(Object.fromEntries(
    Object.entries(results).map(([k, v]) => [k, v.error || v.keys])), null, 1))
  process.exit(0)
}

const en = results[base].flat, ru = results[target].flat
const enPaths = Object.keys(en)
const missing = [], mismatch = [], covered = []
for (const p of enPaths) {
  const r = ru[p]
  if (!r) { missing.push(p); continue }
  if (en[p].fn !== r.fn) { mismatch.push({ p, en: en[p].fn ? 'fn' : 'str', ru: r.fn ? 'fn' : 'str' }); continue }
  covered.push(p)
}

// untranslated = покрыт ключом, но значение осталось базовым (английским)
const untranslated = []
for (const p of covered) {
  const e = en[p].val, r = ru[p].val
  if (typeof e === 'string' && typeof r === 'string' && e === r && /[A-Za-z]{3}/.test(e)) untranslated.push(p)
}

const pct = (n) => (enPaths.length ? ((n / enPaths.length) * 100).toFixed(1) : '0.0')
console.log(JSON.stringify({
  target,
  base,
  enKeys: enPaths.length,
  targetKeys: Object.keys(ru).length,
  covered: covered.length,
  missing: missing.length,
  typeMismatch: mismatch.length,
  sameAsEnglish: untranslated.length,
  pctTranslated: pct(covered.length),
  pctFullyRussian: pct(covered.length - untranslated.length),
  missingSample: missing.slice(0, 15),
  mismatchSample: mismatch.slice(0, 10),
  untranslatedSample: untranslated.slice(0, 15),
}, null, 1))
