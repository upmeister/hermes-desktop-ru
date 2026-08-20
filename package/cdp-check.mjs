// cdp-check.mjs — probe Hermes Desktop via CDP: list targets, count RU markers,
// report uncaught exceptions. Usage: node cdp-check.mjs <port> [--deep]
// node 22 has native WebSocket.
const port = process.argv[2] || '9444'
const base = `http://127.0.0.1:${port}`

async function main() {
  const list = await (await fetch(`${base}/json`)).json()
  const pages = list.filter(t => t.type === 'page')
  console.log(`targets=${list.length} pages=${pages.length}`)
  for (const t of pages.slice(0, 5)) {
    console.log(`  page url=${(t.url || '').slice(0, 90)} title=${(t.title || '').slice(0, 50)}`)
  }
  if (!pages.length) return
  const t = pages[0]
  const ws = new WebSocket(t.webSocketDebuggerUrl)
  let id = 0
  const pending = new Map()
  const send = (method, params = {}) => new Promise((res) => {
    const i = ++id
    pending.set(i, res)
    ws.send(JSON.stringify({ id: i, method, params }))
  })
  const exceptions = []
  ws.addEventListener('message', (ev) => {
    const m = JSON.parse(ev.data)
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || {}); pending.delete(m.id) }
    if (m.method === 'Runtime.exceptionThrown') exceptions.push(m.params.exceptionDetails.text)
  })
  await new Promise((res) => { ws.addEventListener('open', res) })
  await send('Runtime.enable')
  await send('Page.enable')
  // wait for renderer to settle
  await new Promise(r => setTimeout(r, 6000))
  // grab body innerText and srcs
  const evalR = await send('Runtime.evaluate', { expression: 'document.body ? document.body.innerText.slice(0, 3000) : "NOBODY"', returnByValue: true })
  const text = evalR.result ? evalR.result.value : ''
  const ruCount = (text.match(/[А-Яа-яЁё]/g) || []).length
  console.log(`body chars=${text.length} cyrillic=${ruCount}`)
  const findRU = await send('Runtime.evaluate', { expression: `Array.from(document.scripts).map(s=>s.src).filter(u=>/i18n-/i.test(u)).join('\\n')`, returnByValue: true })
  console.log(`i18n scripts:\n${findRU.result ? findRU.result.value.slice(0, 400) : ''}`)
  const ex = await send('Runtime.evaluate', { expression: 'window.__hermesErrors || []', returnByValue: true })
  console.log(`uncaught exceptions during probe: ${exceptions.length}`)
  if (exceptions.length) console.log(exceptions.join('\n'))
  console.log('RU_IN_UI=' + (ruCount > 50 ? 'YES' : 'CHECK'))
  ws.close()
}
main().catch(e => { console.error('ERR', e.message); process.exit(1) })
