// prod-crash-listen.mjs — слушает Runtime.exceptionThrown 120с, пишет тики + финальный JSON.
const port = Number(process.argv[2] || 9444)
const seconds = Number(process.argv[3] || 120)
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
    const stack = d?.stackTrace?.callFrames?.slice(0, 8).map(f => `  at ${f.functionName || '<anon>'} (${f.url.split('/').pop()}:${f.lineNumber}:${f.columnNumber})`).join('\n') || ''
    exceptions.push({ desc: desc.slice(0, 800), stack })
    console.log('EXCEPTION#' + exceptions.length + ': ' + desc.slice(0, 200))
  }
  if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') {
    consoleErrors.push((m.params.entry.text || '').slice(0, 300))
    console.log('LOGERR: ' + consoleErrors[consoleErrors.length - 1].slice(0, 200))
  }
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
    consoleErrors.push((m.params.args || []).map(a => a.value ?? a.description ?? '').join(' ').slice(0, 300))
    console.log('CONSOLEERR: ' + consoleErrors[consoleErrors.length - 1].slice(0, 200))
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

for (let t = 0; t < seconds; t += 10) {
  await sleep(10000)
  const s = await evalJs(`(() => { const b = document.body ? document.body.innerText : ''; return { len: b.length, err: /(error|ошибк|failed|exception)/i.test(b.slice(0, 500)) } })()`)
  console.log(`TICK ${t + 10}s bodyLen=${s?.len ?? '?'} errFlag=${s?.err ?? '?'} exceptions=${exceptions.length}`)
  if (exceptions.length > 0) break
}
console.log('FINAL: ' + JSON.stringify({ exceptions, consoleErrors: consoleErrors.slice(0, 8) }, null, 1))
ws.close()
process.exit(0)
