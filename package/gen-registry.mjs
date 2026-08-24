#!/usr/bin/env node
// gen-registry.mjs — извлекает структурный реестр якорей из git-патча ru-mod-v3.patch.
//
// Ключевая идея (вариант C): хунк git-патча = последовательность под-правок, разделённых
// контекстными (нетронутыми) строками. Одни операции могут идти НЕ подряд: между двумя
// удалениями могут стоять контекстные строки. Поэтому мы:
//   1. парсим каждый хунк и разбиваем его на под-группы по контекстным строкам;
//   2. для каждой под-группы с rem.len == add.len делаем ПОСТРОЧНЫЕ пары
//      (каждая строка — независимый якорь: переживает сдвиги/вставки апстрима);
//   3. иначе — блок (развёрнутые строки 1->N и прочее).
// Смежность для пары не нужна: движок ищет конкретную строку в любом месте файла.
//
// Вход: путь к .patch (или несколько), выход: registry.json + apply-hardcodes.mjs.
import fs from 'node:fs'
import path from 'node:path'

const patchPath = process.argv[2]
const outPath = process.argv[3] || path.join(path.dirname(patchPath), 'registry.json')
const patch = fs.readFileSync(patchPath, 'utf8')

const blocks = patch.split(/^diff --git /m).slice(1)

function parseHunk(body) {
  const lines = body.split('\n')
  const ctx = []
  let state = 'header'
  for (const l of lines) {
    if (state === 'header') {
      if (l.startsWith('@@')) state = 'body'
      continue
    }
    ctx.push(l)
  }
  while (ctx.length && ctx[ctx.length - 1] === '') ctx.pop()
  return ctx
}

let rules = []
let pairRules = 0, blockRules = 0, insertRules = 0

for (const blk of blocks) {
  const firstLine = blk.split('\n', 1)[0]
  const m = firstLine.match(/^a\/\S+ b\/(\S+)/)
  if (!m) { continue }
  const file = m[1]
  if (!file.startsWith('apps/desktop/')) continue
  const body = blk.slice(firstLine.length).replace(/^\n/, '')
  const parts = body.split(/^@@ /m).slice(1)
  const hunks = parts.map(raw => parseHunk('@@ ' + raw))

  let fileRuleIdx = 0
  const nextId = () => `${file.split('/').pop()}-${++fileRuleIdx}`

  for (const ctx of hunks) {
    // Split hunk into sub-groups on context lines. A context line (space prefix
    // or the @@ header) breaks a run of changes. Track lastCtx = the last
    // untouched line, used as the anchor for pure inserts.
    const groups = [] // [{removed:[], added:[], anchor:str}]
    let cur = null
    let lastCtx = ''
    for (const l of ctx) {
      const isAdd = l.startsWith('+') && !l.startsWith('+++')
      const isDel = l.startsWith('-') && !l.startsWith('---')
      const isCtx = !(isAdd && isDel) && !l.startsWith('@@') && !(isAdd || isDel) // context or spacer
      if (l.startsWith('@@')) continue
      if (l.startsWith('-') && !l.startsWith('---')) { if (!cur) { cur = { removed: [], added: [], anchor: lastCtx }; groups.push(cur) }; cur.removed.push(l.slice(1)); continue }
      if (l.startsWith('+') && !l.startsWith('+++')) { if (!cur) { cur = { removed: [], added: [], anchor: lastCtx }; groups.push(cur) }; cur.added.push(l.slice(1)); continue }
      // context line: close out current group
      cur = null
      if (l.slice(1).trim() !== '') lastCtx = l.slice(1) // keep last NON-EMPTY untouched line as insert anchor
    }
    // trim trailing empties inside each group
    for (const g of groups) {
      while (g.removed.length && g.removed[g.removed.length - 1] === '') g.removed.pop()
      while (g.added.length && g.added[g.added.length - 1] === '') g.added.pop()
    }

    for (const g of groups) {
      const rem = g.removed, add = g.added
      if (rem.length === 0 && add.length === 0) continue
      if (rem.length === 0) {
        // pure insert after the last untouched context line (g.anchor)
        if (!g.anchor.trim()) { console.error(`WARN: no anchor for insert in ${file}`); continue }
        rules.push({ id: nextId(), file, mode: 'insert-after', insertAfterLine: g.anchor, after: add })
        insertRules++
        continue
      }
      if (rem.length === add.length) {
        for (let i = 0; i < rem.length; i++) {
          rules.push({ id: nextId(), file, before: [rem[i]], after: [add[i]] })
          pairRules++
        }
      } else {
        rules.push({ id: nextId(), file, before: rem, after: add })
        blockRules++
      }
    }
  }
}

// ---- Fold duplicates: same (file, before) with IDENTICAL after -> all:true ----
const byKey = new Map()
for (const r of rules) {
  const key = r.file + '\u0000' + JSON.stringify(r.before || null)
  if (!byKey.has(key)) byKey.set(key, [])
  byKey.get(key).push(r)
}
const folded = []
for (const group of byKey.values()) {
  if (group.length === 1) { folded.push(group[0]); continue }
  const afters = new Set(group.map(r => JSON.stringify(r.after || null)))
  if (afters.size === 1) {
    const base = { ...group[0], all: true }
    folded.push(base)
  } else {
    folded.push(...group)
  }
}
rules.length = 0
rules.push(...folded)

// Sort by file then index
rules.sort((a, b) => (a.file < b.file ? -1 : a.file > b.file ? 1 : 0))

// ---- Manual override layer (overrides.json next to the output) ----
const overridePath = outPath.replace(/registry\.json$/, 'overrides.json')
if (fs.existsSync(overridePath)) {
  const ovr = JSON.parse(fs.readFileSync(overridePath, 'utf8'))
  for (const o of ovr) {
    if (o && o.delete) {
      const before = rules.length
      rules = rules.filter(r => r.id !== o.delete)
      console.log(`override: removed ${o.delete} (${before - rules.length == 1 ? 'ok' : 'NOT FOUND'})`)
    }
  }
  const byId = new Map(rules.map(r => [r.id, r]))
  for (const o of ovr) {
    if (!o || o.delete) continue
    const existing = byId.get(o.id)
    if (existing) { Object.assign(existing, o); byId.set(o.id, existing) }
    else { rules.push(o); byId.set(o.id, o) }
  }
}

// Default severity after overrides so an explicit stamp wins.
// insert-after changes control flow (imports / remaps) — critical.
// Everything else is a UI literal swap — cosmetic.
for (const r of rules) {
  if (r.severity) continue
  r.severity = r.mode === 'insert-after' ? 'critical' : 'cosmetic'
}

fs.writeFileSync(outPath, JSON.stringify(rules, null, 1) + '\n')
console.log(`registry: ${outPath}`)
console.log(`rules total=${rules.length} pair=${pairRules} block=${blockRules} insert=${insertRules} files=${new Set(rules.map(r=>r.file)).size}`)