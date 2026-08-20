// deps-health.mjs <repoRoot> — checks that key packages resolve from the repo.
// exit 0 = healthy, 1 = missing. Prints one line per missing package.
// Used by install-asar.ps1 to decide whether to rebuild node_modules via npm ci.
import { createRequire } from 'node:module'
import process from 'node:process'
const root = process.argv[2] || process.cwd()
const req = createRequire(root + '/package.json')
const probes = ['vite', '@electron/asar', '@tabler/icons-react', 'react', 'electron-builder']
let bad = false
for (const p of probes) {
  try {
    req.resolve(p)
  } catch {
    console.log(`missing: ${p}`)
    bad = true
  }
}
process.exit(bad ? 1 : 0)
