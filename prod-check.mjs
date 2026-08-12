// prod-check.mjs — быстрая CDP-проверка прод-приложения: процесс, окно, рендерер, exceptions.
// БЕЗ отправки сообщений (рабочая среда пользователя).
const port = Number(process.argv[2] || 9444)
const sleep = ms => new Promise(r => setTimeout(r, ms))

let targets
for (let i = 0; i < 60; i++) {
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
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data)
  if (m.id != null && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return }
  if (m.method === 'Runtime.exceptionThrown') {
    exceptions.push(m.params.exceptionDetails?.exception?.description || m.params.exceptionDetails?.text || 'exception')
  }
})
await new Promise(r => ws.addEventListener('open', r))
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })) })
const evalJs = async expression => {
  const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })
  return r.result?.result?.value
}
await send('Runtime.enable')

// ждём рендерер: body с контентом
let body = '', title = ''
for (let i = 0; i < 60; i++) {
  body = (await evalJs(`document.body ? document.body.innerText.slice(0, 400) : ''`)) || ''
  title = (await evalJs(`document.title`)) || ''
  if (body.length > 20 || title) break
  await sleep(1000)
}
const hasRu = /[а-яА-ЯёЁ]{3,}/.test(body)
const hasEn = /[A-Za-z]{3,}/.test(body)
console.log(JSON.stringify({
  pass: exceptions.length === 0 && body.length > 20,
  stage: 'done',
  exceptions,
  checks: { bodyLen: body.length, hasRu, hasEn, title },
  bodySnippet: body.slice(0, 200)
}, null, 1))
ws.close()
process.exit(exceptions.length === 0 && body.length > 20 ? 0 : 1)
