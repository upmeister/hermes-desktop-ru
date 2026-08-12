// prod-crash-catch.mjs — ловит краш рендерера при переходе в Провайдеры.
// 1) читает текущее состояние UI; 2) кликает по тексту «Провайдеры» → «Пользовательские провайдеры»;
// 3) собирает Runtime.exceptionThrown (со стеком) и console-ошибки; 4) печатает JSON.
const port = Number(process.argv[2] || 9444)
const sleep = ms => new Promise(r => setTimeout(r, ms))

let targets
for (let i = 0; i < 30; i++) {
  try {
    targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()
    if (targets.some(t => t.type === 'page')) break
  } catch {}
  await sleep(1000)
}
const page = targets?.find(t => t.type === 'page')
if (!page) { console.log(JSON.stringify({ pass: false, stage: 'cdp', reason: 'no page target' })); process.exit(1) }

const ws = new WebSocket(page.webSocketDebuggerUrl)
let id = 0
const pending = new Map()
const exceptions = []
const consoleErrors = []
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data)
  if (m.id != null && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return }
  if (m.method === 'Runtime.exceptionThrown') {
    const d = m.params.exceptionDetails
    const desc = d?.exception?.description || d?.text || 'exception'
    const stack = d?.stackTrace?.callFrames?.slice(0, 6).map(f => `  at ${f.functionName || '<anon>'} (${f.url.split('/').pop()}:${f.lineNumber}:${f.columnNumber})`).join('\n') || ''
    exceptions.push({ desc: desc.slice(0, 500), stack })
  }
  if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') {
    consoleErrors.push((m.params.entry.text || '').slice(0, 300))
  }
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
    consoleErrors.push((m.params.args || []).map(a => a.value ?? a.description ?? '').join(' ').slice(0, 300))
  }
})
await new Promise(r => ws.addEventListener('open', r))
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })) })
const evalJs = async expression => {
  try {
    const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })
    return r.result?.result?.value
  } catch { return null }
}
await send('Runtime.enable')
await send('Log.enable')

const stateJs = `(() => {
  const body = document.body ? document.body.innerText : ''
  return { len: body.length, snippet: body.slice(0, 300), hasErr: /(error|ошибк|failed|exception)/i.test(body.slice(0, 800)) }
})()`
const before = await evalJs(stateJs)

// клик по «Провайдеры», потом «Пользовательские провайдеры»
const clickJs = label => `(() => {
  const els = [...document.querySelectorAll('button, a, [role="menuitem"], [role="tab"], [role="button"], div, span')]
  const el = els.find(e => {
    const t = (e.textContent || '').trim()
    return t === '${label}' && e.offsetParent !== null
  })
  if (!el) return 'not-found: ${label}'
  el.click()
  return 'clicked: ${label}'
})()`
const click1 = await evalJs(clickJs('Провайдеры'))
await sleep(1500)
const click2 = await evalJs(clickJs('Пользовательские провайдеры'))
await sleep(1500)
const mid = await evalJs(stateJs)
// если первый клик не сработал (уже в настройках / другой текст) — пробуем варианты
if (click1 === 'not-found: Провайдеры' || click2 === 'not-found: Пользовательские провайдеры') {
  for (const lbl of ['Провайдеры', 'провайдеры', 'Providers', 'Custom endpoints', 'Пользовательские провайдеры', 'Свои endpoints', 'Свои провайдеры']) {
    const r = await evalJs(clickJs(lbl))
    if (!r.startsWith('not-found')) { await sleep(1500); break }
  }
}
await sleep(4000)
const after = await evalJs(stateJs)
console.log(JSON.stringify({ pass: true, click1, click2, before, mid, after, exceptions, consoleErrors: consoleErrors.slice(0, 8) }, null, 1))
ws.close()
process.exit(0)
