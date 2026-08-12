// probe-ru.mjs - find the chunk containing the RU marker ('Применить') in dist/assets.
// Usage: node probe-ru.mjs <path-to-dist-assets>
// Separate .mjs file on purpose: inline `node -e` inside PS breaks on Windows
// backslash paths (\U -> JS SyntaxError "Expected ',', got 'ident'").
import fs from 'fs'
import path from 'path'

const assets = process.argv[2]
const marker = 'Применить' // RU marker proving the clone build had the ru-mod
let found = null
for (const f of fs.readdirSync(assets)) {
  if (!f.endsWith('.js')) continue
  const s = fs.readFileSync(path.join(assets, f), 'utf8')
  if (s.includes(marker)) { found = f; break }
}
console.log(found ? found : 'NONE')
