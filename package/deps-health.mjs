// deps-health.mjs <repoRoot> — checks that key packages resolve from the repo.
// exit 0 = healthy, 1 = missing. Prints one line per missing package.
// Resolution: tries the repo root AND the desktop workspace (apps/desktop) —
// npm hoists workspaces into nested node_modules, so root-only resolution
// would false-positive on workspace-only deps like @rolldown/plugin-babel.
import { createRequire } from 'node:module'
import process from 'node:process'
import { existsSync } from 'node:fs'
import { join } from 'node:path'

const root = process.argv[2] || process.cwd()
const candidates = [root, join(root, 'apps', 'desktop')].filter(p => existsSync(join(p, 'package.json')))
const probes = ['vite', '@electron/asar', '@tabler/icons-react', 'react', 'electron-builder', '@rolldown/plugin-babel']
let bad = false
for (const p of probes) {
  let found = false
  for (const base of candidates) {
    try {
      createRequire(join(base, 'package.json')).resolve(p)
      found = true
      break
    } catch {
      // try next base
    }
  }
  if (!found) {
    console.log(`missing: ${p}`)
    bad = true
  }
}
process.exit(bad ? 1 : 0)