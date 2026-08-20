// cdp-markers.mjs — verify specific RU markers from our mod are visible in the live UI.
// Usage: node cdp-markers.mjs <port>
const PORT = process.argv[2] || '9444'
const markers = [
  'Применить',          // i18n probe marker (settings apply)
  'Подключения',        // connections tab
  'Новая сессия',       // NEW_SESSION_TITLE hardcode
  'Рабочие материалы',  // artifacts tab
  'Сессии',             // sidebar
  'Обслуживание',       // maintenance tab
  'Это устройство',     // local connection (v3.20)
  'Опасная зона',       // uninstall section (hardcode)
]
async function main() {
  const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json()
  const t = list.find(x => x.type === 'page')
  if (!t) { console.log('NO PAGE'); return }
  const ws = new WebSocket(t.webSocketDebuggerUrl)
  let id = 0
  const pending = new Map()
  const send = (m, p = {}) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method: m, params: p })) })
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || {}); pending.delete(m.id) } })
  await new Promise(res => ws.addEventListener('open', res))
  await send('Runtime.enable')
  await new Promise(r => setTimeout(r, 4000))
  const full = await send('Runtime.evaluate', { expression: 'document.body ? document.body.innerText : ""', returnByValue: true })
  const text = full.result ? full.result.value || '' : ''
  console.log(`total innerText chars: ${text.length}`)
  for (const m of markers) console.log(`${text.includes(m) ? 'OK  ' : 'MISS'} ${m}`)
  ws.close()
}
main().catch(e => { console.error('ERR', e.message); process.exit(1) })
