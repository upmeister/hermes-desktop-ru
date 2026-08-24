#!/usr/bin/env node
// apply-hardcodes.mjs — применяет хардкод-переводы ru-мода структурным реестром якорей
// вместо git apply --3way. Почему вариант C (см. план 2026-08-09-ru-mod-revival-plan, фаза 10):
// git apply --3way в SHALLOW-клоне НЕ сообщает о невозможности чистого применения — он
// накладывает конфликт-маркеры (<<<<<<< ours / >>>>>>> theirs) прямо в файлы и build падает
// на vite "Encountered diff marker". Реестр якорей:
//   - ищет ПОЛНЫЕ уникальные блоки строк (before), а не смещения строк, — переживает сдвиги
//     апстрима выше по файлу;
//   - после замены становится идемпотентным (after уже есть -> skip);
//   - якорь не найден и after не найден -> ПОНЯТНЫЙ MISSING-отчёт, ноль молчаливых поломок;
//   - режим --doctor ничего не пишет: сухая проверка (используется в install-asar.ps1 перед build).
//
// Severity (с 24.08.2026, гейт 1–2):
//   cosmetic (дефолт) — замена UI-литерала. MISSING/AMBIGUOUS = пятно по-английски.
//     apply не пишет правило и НЕ валит процесс. doctor — WARN.
//   critical / code — insert, импорт, смена control flow. Пропуск = фича мода выключена.
//     apply не пишет. doctor/install FAIL только если пропал сам файл (MISSING_FILE).
//   Зона COSMETIC_ZONES (hermes-bots/plugin.js) всегда cosmetic: из неё нельзя FAIL.
//   overrides.json рядом с registry мержится в рантайме (severity/delete/новые id) —
//     не обязательно перегонять gen-registry, чтобы классификация доехала.
//
// Формат реестра (registry.json):
//   [ { file, id, before: [lines], after: [lines] | null, severity?, all?, mode? } ]
//   file — путь ОТНОСИТЕЛЬНО srcRoot (например apps/desktop/src/...)
//   before — точная последовательность строк (без EOL) в текущей форме апстрима (англ.)
//   after — заменяющие строки. null => чистая вставка (mode:'insert-after' с insertAfterLine)
//   ПОДДЕРЖИВАЕМЫЕ режимы:
//     default : before найдён уникально -> заменить на after (после уже есть -> skip)
//     insert-after : insertAfterLine — уникальная строка, ПОСЛЕ которой вставить after
//
import fs from 'node:fs'
import path from 'node:path'

const [,, srcRoot, regPath, maybeDoc] = process.argv
const doctor = maybeDoc === '--doctor'
if (!srcRoot || !regPath) {
  console.error('usage: node apply-hardcodes.mjs <repoRoot> <registry.json> [--doctor]')
  process.exit(2)
}
if (!fs.existsSync(regPath)) {
  console.error(`registry not found: ${regPath}`)
  process.exit(2)
}

let rules = JSON.parse(fs.readFileSync(regPath, 'utf8'))
if (!Array.isArray(rules)) {
  console.error('registry must be a JSON array of rules')
  process.exit(2)
}

// Files whose every rule is cosmetic, even if someone stamped severity:critical.
// hermes-bots/plugin.js — скомпилированный плагин, апстрим переписывает часто;
// 200 коротких литералов не должны стопорить установку.
const COSMETIC_ZONES = new Set([
  'apps/desktop/src/plugins/hermes-bots/plugin.js',
])

// Fallback, если overrides ещё не доехали до registry.json.
const DEFAULT_CRITICAL_IDS = new Set([
  'connection-registry.ts-2',
  'plugin.tsx-1',
  'boot-failure-i18n-then',
  'boot-failure-i18n-catch',
  'boot-failure-i18n-savelocale',
])

function normFile(f) {
  return String(f || '').replace(/\\/g, '/')
}

function mergeOverrides(list, overridePath) {
  if (!fs.existsSync(overridePath)) return list
  let ovr
  try {
    ovr = JSON.parse(fs.readFileSync(overridePath, 'utf8'))
  } catch (e) {
    console.error(`overrides.json: не разобрать (${e.message}) — продолжаю без него`)
    return list
  }
  if (!Array.isArray(ovr)) return list
  let out = list.slice()
  for (const o of ovr) {
    if (o && o.delete) {
      out = out.filter(r => r.id !== o.delete)
    }
  }
  const byId = new Map(out.map(r => [r.id, r]))
  for (const o of ovr) {
    if (!o || o.delete) continue
    const existing = byId.get(o.id)
    if (existing) {
      Object.assign(existing, o)
    } else {
      out.push(o)
      byId.set(o.id, o)
    }
  }
  return out
}

rules = mergeOverrides(rules, path.join(path.dirname(regPath), 'overrides.json'))

function effectiveSeverity(rule) {
  if (COSMETIC_ZONES.has(normFile(rule.file))) return 'cosmetic'
  if (rule.severity === 'critical' || rule.severity === 'code') return 'critical'
  if (DEFAULT_CRITICAL_IDS.has(rule.id)) return 'critical'
  return 'cosmetic'
}

function readUtf8(p) {
  const buf = fs.readFileSync(p)
  const eol = buf.includes(Buffer.from('\r\n')) ? '\r\n' : '\n'
  return { content: buf.toString('utf8'), eol }
}

// Normalize any EOL to \n for matching; we'll re-emit with the file's EOL.
function normalize(s) { return s.replace(/\r\n/g, '\n') }

function findBlock(contentLines, block, startIdx = 0) {
  // block: array of lines (no EOL, content already normalized)
  if (!block.length) return -1
  outer:
  for (let i = startIdx; i + block.length <= contentLines.length; i++) {
    for (let j = 0; j < block.length; j++) {
      if (contentLines[i + j].replace(/\s+$/, '') !== block[j].replace(/\s+$/, '')) continue outer
    }
    return i
  }
  return -1
}

function countOccurrences(contentLines, block) {
  let n = 0
  let idx = findBlock(contentLines, block)
  while (idx !== -1) { n++; idx = findBlock(contentLines, block, idx + 1) }
  return n
}

const results = []

for (const rule of rules) {
  const { id, file, before, after, mode, insertAfterLine } = rule
  const sev = effectiveSeverity(rule)
  const abs = path.join(srcRoot, file)
  if (!fs.existsSync(abs)) {
    results.push({ id, status: 'MISSING_FILE', file, why: 'файл не найден', severity: sev })
    continue
  }
  const { content, eol } = readUtf8(abs)
  const contentLines = normalize(content).split('\n')
  // drop final empty line artifact of trailing newline
  if (contentLines.length > 1 && contentLines[contentLines.length - 1] === '') contentLines.pop()

  let status
  let idx
  if (mode === 'insert-after') {
    const anchor = [insertAfterLine]
    const n = countOccurrences(contentLines, anchor)
    if (n === 0) {
      idx = -1
    } else if (n > 1) {
      results.push({ id, status: 'AMBIGUOUS', file, why: `якорь-вставки не уникален (${n})`, severity: sev })
      continue
    } else {
      idx = findBlock(contentLines, anchor)
    }
    if (idx === -1) {
      const afterLines = (after || []).slice(0, 1)
      const already = afterLines.length && afterLines[0] && countOccurrences(contentLines, afterLines) > 0
      if (already) {
        results.push({ id, status: 'OK_ALREADY', file, why: 'вставка уже присутствует', severity: sev })
        continue
      }
      results.push({ id, status: 'MISSING', file, why: `якорь вставки '${(insertAfterLine || '').slice(0, 60)}' не найден`, severity: sev })
      continue
    }
    const ins = (after || []).map(l => l)
    let alreadyThere = true
    for (let j = 0; j < ins.length; j++) {
      if (contentLines[idx + 1 + j] === undefined ||
          contentLines[idx + 1 + j].replace(/\s+$/, '') !== ins[j].replace(/\s+$/, '')) {
        alreadyThere = false
        break
      }
    }
    if (alreadyThere) {
      results.push({ id, status: 'OK_ALREADY', file, why: 'блок уже сразу после якоря', severity: sev })
      continue
    }
    if (!doctor) {
      contentLines.splice(idx + 1, 0, ...ins)
      fs.writeFileSync(abs, contentLines.join(eol) + (content.endsWith('\n') ? eol : ''))
    }
    status = 'APPLIED'
  } else {
    const n = countOccurrences(contentLines, before || [])
    if (n === 0) {
      const afterN = (after || []).length && after[0] ? countOccurrences(contentLines, after || []) : 0
      if (afterN > 0) {
        results.push({ id, status: 'OK_ALREADY', file, why: 'замена уже применена', severity: sev })
        continue
      }
      results.push({ id, status: 'MISSING', file, why: `блок не найден (${(before || []).length} строк), после-блок тоже`, severity: sev })
      continue
    }
    if (n > 1 && !rule.all) {
      results.push({ id, status: 'AMBIGUOUS', file, why: `блок найден ${n} раз`, severity: sev })
      continue
    }
    idx = -1
    let replaced = 0
    while ((idx = findBlock(contentLines, before, idx + 1)) !== -1) {
      if (doctor) { idx += before.length; replaced++; continue }
      contentLines.splice(idx, before.length, ...(after || []))
      replaced++
      idx += (after || []).length - 1
    }
    if (!doctor && replaced > 0) {
      fs.writeFileSync(abs, contentLines.join(eol) + (content.endsWith('\n') ? eol : ''))
    }
    status = 'APPLIED'
  }
  results.push({ id, status, file, severity: sev })
}

// Summary
const by = {}
for (const r of results) by[r.status] = (by[r.status] || 0) + 1

const problems = results.filter(r => r.status !== 'APPLIED' && r.status !== 'OK_ALREADY')
const critMissingFile = problems.filter(r => r.severity === 'critical' && r.status === 'MISSING_FILE').length
const critMissing = problems.filter(r => r.severity === 'critical' && (r.status === 'MISSING' || r.status === 'MISSING_FILE')).length
const critAmb = problems.filter(r => r.severity === 'critical' && r.status === 'AMBIGUOUS').length
const cosMissing = problems.filter(r => r.severity !== 'critical' && (r.status === 'MISSING' || r.status === 'MISSING_FILE')).length
const cosAmb = problems.filter(r => r.severity !== 'critical' && r.status === 'AMBIGUOUS').length

console.log(
  `[apply-hardcodes] ${doctor ? 'DOCTOR' : 'APPLY'} rules=${rules.length} ` +
  Object.entries(by).map(([k, v]) => `${k}=${v}`).join(' ')
)
console.log(
  `GATE critical_missing_file=${critMissingFile} critical_missing=${critMissing} ` +
  `critical_ambiguous=${critAmb} cosmetic_missing=${cosMissing} cosmetic_ambiguous=${cosAmb}`
)

if (problems.length) {
  console.log('--- PROBLEMS ---')
  for (const r of problems) {
    const tag = r.severity === 'critical' ? '[critical] ' : ''
    console.log(`  [${r.status}] ${tag}${r.file} :: ${r.id} :: ${r.why || ''}`)
  }
}

if (doctor) {
  // ненулевой код = «есть PROBLEMS» (установщик рисует WARN). FAIL решает install-asar по GATE.
  process.exit(problems.length ? 1 : 0)
}

// apply: косметика не валит процесс (правила уже пропущены, файлы консистентны).
// exit 1 только если критичное правило не смогли применить — вызывающий может остановиться.
if (critMissingFile > 0) {
  process.exit(1)
}
console.log(problems.length ? 'apply: косметические пропуски оставлены как есть' : 'all rules OK')
process.exit(0)