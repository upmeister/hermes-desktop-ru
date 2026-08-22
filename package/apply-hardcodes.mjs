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
// Формат реестра (registry.json):
//   [ { file, id, before: [lines], after: [lines] | null } ]
//   file — путь ОТНОСИТЕЛЬНО srcRoot (например apps/desktop/src/...)
//   before — точная последовательность строк (без EOL) в текущей форме апстрима (англ.)
//   after — заменяющие строки. null => чистая вставка (before вставляется дословно? нет:
//          для вставки используется mode:'insert-after' с anchorLine)
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

const rules = JSON.parse(fs.readFileSync(regPath, 'utf8'))
if (!Array.isArray(rules)) {
  console.error('registry must be a JSON array of rules')
  process.exit(2)
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
let failCount = 0

for (const rule of rules) {
  const { id, file, before, after, mode, insertAfterLine } = rule
  const abs = path.join(srcRoot, file)
  if (!fs.existsSync(abs)) {
    results.push({ id, status: 'MISSING_FILE', file, why: 'файл не найден' })
    failCount++
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
      // already applied? check that 'after' first line exists after nothing...
      idx = -1
    } else if (n > 1) {
      status = 'AMBIGUOUS'
      results.push({ id, status, file, why: `якорь-вставки не уникален (${n})` })
      failCount++
      continue
    } else {
      idx = findBlock(contentLines, anchor)
    }
    if (idx === -1) {
      // idempotency: is the inserted block already present right after the anchor position?
      const afterLines = (after || []).slice(0, 1)
      const already = afterLines.length && afterLines[0] && countOccurrences(contentLines, afterLines) > 0
      if (already) {
        results.push({ id, status: 'OK_ALREADY', file, why: 'вставка уже присутствует' })
        continue
      }
      results.push({ id, status: 'MISSING', file, why: `якорь вставки '${(insertAfterLine || '').slice(0, 60)}' не найден` })
      failCount++
      continue
    }
    // Idempotency: block already right after the anchor? (anchor found this run)
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
      results.push({ id, status: 'OK_ALREADY', file, why: 'блок уже сразу после якоря' })
      continue
    }
    // insert after idx (the anchor line)
    if (!doctor) {
      contentLines.splice(idx + 1, 0, ...ins)
      fs.writeFileSync(abs, contentLines.join(eol) + (content.endsWith('\n') ? eol : ''))
    }
    status = 'APPLIED'
  } else {
    // default replace
    const n = countOccurrences(contentLines, before || [])
    if (n === 0) {
      // maybe already applied (after present)
      const afterN = (after || []).length && after[0] ? countOccurrences(contentLines, after || []) : 0
      if (afterN > 0) {
        results.push({ id, status: 'OK_ALREADY', file, why: 'замена уже применена' })
        continue
      }
      results.push({ id, status: 'MISSING', file, why: `блок не найден (${(before || []).length} строк), после-блок тоже` })
      failCount++
      continue
    }
    if (n > 1 && !rule.all) {
      results.push({ id, status: 'AMBIGUOUS', file, why: `блок найден ${n} раз` })
      failCount++
      continue
    }
    // rule.all: заменяем ВСЕ вхождения (одинаковая замена в нескольких местах)
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
  results.push({ id, status, file, why: status === 'AMBIGUOUS' ? results[results.length - 1].why : undefined })
}

// Summary
const by = {}
for (const r of results) by[r.status] = (by[r.status] || 0) + 1
const criticalIds = new Set(rules.filter(r => r.severity === 'critical').map(r => r.id))
const criticalMissing = results.filter(r =>
  (r.status === 'MISSING' || r.status === 'MISSING_FILE') && criticalIds.has(r.id)).length
console.log(`[apply-hardcodes] ${doctor ? 'DOCTOR' : 'APPLY'} rules=${rules.length} ` +
  Object.entries(by).map(([k, v]) => `${k}=${v}`).join(' ') + ` CRITICAL_MISSING=${criticalMissing}`)

if (failCount > 0 || Object.keys(by).includes('AMBIGUOUS')) {
  console.log('--- PROBLEMS ---')
  for (const r of results) {
    if (r.status !== 'APPLIED' && r.status !== 'OK_ALREADY') {
      const tag = criticalIds.has(r.id) ? '[critical] ' : ''
      console.log(`  [${r.status}] ${tag}${r.file} :: ${r.id} :: ${r.why || ''}`)
    }
  }
  process.exit(1)
}
console.log('all rules OK')
