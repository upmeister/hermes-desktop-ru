# 🇷🇺 Hermes Desktop — Russian mod

[🇬🇧 English](README.en.md) · [🇷🇺 Русский](README.md)

Full Russian localization for [Hermes Desktop](https://github.com/NousResearch/hermes-agent).

[![Hermes Desktop](https://img.shields.io/badge/Hermes_Desktop-0.20.5-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![npm](https://img.shields.io/npm/v/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![npm](https://img.shields.io/npm/dm/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**Latest: [v1.2.0](https://github.com/upmeister/hermes-desktop-ru/releases/tag/v1.2.0) · Hermes Desktop 0.20.5 · 2026-08-25**

Hermes Desktop has **no Russian locale in the current release line** (upstream `ru` PRs have sat open since July). i18n-only packs translate the catalog and leave hardcoded strings in components, settings field labels, Bots/kanban, and the Electron main process.

This is not a portable / prebuilt installer patch. It expects a **source checkout** (`hermes desktop` / `git clone`) and rebuilds `app.asar` inside that clone.

**Windows is the supported path** (author-tested). **Linux and macOS are experimental**: the installer resolves POSIX clone/asar layouts, but the author has not run them on a live Desktop. We never patch a notarized `.app` or website AppImage — only `apps/desktop/release/` next to the clone.

## Screens

![Chat](docs/screenshots/chat.png)

![Settings](docs/screenshots/settings.png)

![Bots / kanban](docs/screenshots/bots-kanban.png)

## Why not just a locale file

| | i18n-only pack | this mod |
|---|---|---|
| Catalog keys | ✅ (~2200+) | ✅ full catalog |
| Hardcoded component strings | ❌ | ✅ |
| Bots / kanban / main-process | ❌ | ✅ |
| After `hermes update` | new UI stays English | re-run `hermes-desktop-ru install` |

- **865-rule structural registry** rewrites unique `before → after` blocks in renderer, `ru-constants.ts`, Bots, kanban, and `electron/main.ts`.
- **Doctor-gated installer** — dry-run before any write. Cosmetic misses (including an ambiguous short literal in Bots) warn — that spot stays English. Install fails only if a *critical file* is gone (kanban / connection-registry). A failed `npm run build` is the real hard stop.
- **Survives `hermes update`**: restore tracked sources to stock → doctor → apply → register `ru` → rebuild `dist` → repack `asar` (original kept as `.stock.bak`).

## Why structural anchors, not `git apply`

`git apply --3way` on a shallow clone can **exit 0** while leaving `<<<<<<<` conflict markers in the tree. Vite then dies with "Encountered diff marker", and the markers poison the *next* mod too.

The registry instead:

- matches **full unique string blocks** anywhere in the file (survives inserts above);
- is idempotent and EOL-preserving;
- reports `MISSING` / `AMBIGUOUS`; cosmetic skips, a missing critical *file* fails closed;
- `EXPECTED_COMMIT` warns (does not block) when HEAD moved past the build base.

## Installer layout

Source of truth is Node: `package/install.mjs`. `bin/hermes-desktop-ru.mjs` just forwards argv. PowerShell / BAT stay as a double-click wrapper on Windows; `install.sh` does the same on POSIX.

Clone resolution, first hit wins:

1. `--root` / `-Root`
2. `HERMES_AGENT_ROOT`
3. `HERMES_INSTALL_DIR`
4. `$HERMES_HOME/hermes-agent`
5. `~/.hermes/hermes-agent`
6. `/usr/local/lib/hermes-agent` (Linux root/FHS install)
7. `%LOCALAPPDATA%\hermes\hermes-agent`

Asar resolution is **clone-local only** (`apps/desktop/release/`):

- `win-unpacked/resources/app.asar`
- `linux-unpacked/resources/app.asar`
- `mac[-arm64|-x64]/Hermes.app/Contents/Resources/app.asar`

`/Applications/Hermes.app` and a website AppImage are out of scope on purpose (Gatekeeper / you become an unofficial Hermes distributor).

`package.json` no longer sets `"os": ["win32"]`. npm will install the CLI on Linux/macOS; that does not mean those platforms are supported at Windows quality. Process-kill and uninstall there are best-effort. After swapping asar inside a self-built `.app`, the installer runs ad-hoc `codesign --sign -` — not Apple notarization.

CI: `check.yml` runs `node --check`, parses `registry.json`, and `node package/install.mjs --self-test`. `experimental-posix.yml` is `workflow_dispatch` only: self-test on ubuntu+macos, optional `doctor` against a shallow `hermes-agent` clone (cosmetic WARN on HEAD is expected; FAIL only if a critical file vanished). It does **not** `npm run pack` Hermes.

## Install

Node.js 18+, Hermes Desktop **closed**, source checkout.

```bash
npm install -g hermes-desktop-ru
hermes-desktop-ru install
```

| Command | |
|---|---|
| `hermes-desktop-ru install` | install / re-install. Restores tracked clone sources to HEAD |
| `hermes-desktop-ru doctor` | dry compatibility check — no writes, no process kill, no `git restore` |
| `hermes-desktop-ru uninstall` | restore packaged `app.asar` from `.stock.bak` (clone untouched) |
| `hermes-desktop-ru version` | package version (from `package.json`) |
| `hermes-desktop-ru help` | help |

```bash
hermes-desktop-ru install --root /path/to/hermes-agent
```

(`HERMES_AGENT_ROOT` / `HERMES_HOME` work too.) Or unpack the [release zip](https://github.com/upmeister/hermes-desktop-ru/releases) and run `install.bat` / `install.sh` / `node install.mjs`.

The clone must already contain a packaged Desktop (`hermes desktop` or `cd apps/desktop && npm run pack`). Failed `npm run build` is a hard error. To reuse a bundled `package/dist` (may not match this upstream): `--allow-stale-dist`.

## After `hermes update`

```text
hermes update  →  hermes-desktop-ru install  →  launch
```

`hermes update` does **not** rebuild the already-installed asar. A stale Russian bundle can look alive — it is stale. Always re-run the installer.

`install` runs `git restore` on tracked files in the clone. Other source-level mods in that checkout will not survive. `doctor` does not restore or kill the app.

## Doctor

`hermes-desktop-ru doctor` writes nothing, does not stop Desktop, does not run `npm ci`. It reports:

- `OK` — every registry rule matches;
- `WARN` — cosmetic miss or ambiguous literal (install proceeds; that spot stays English). `hermes-bots/plugin.js` is always this zone;
- `FAIL` — a critical rule's *file* is gone (kanban / connection-registry). Missing or ambiguous *text* is never FAIL.

If the working tree is dirty, doctor warns and checks the **current** tree.

## Safety

- Local only: no backend, no telemetry, no network from the installer.
- Doctor gate before writes; tracked sources restored to stock on **install** only.
- Process kill is path-restricted to the clone / resolved pack. The installer does not `killall hermes` (that would take down the CLI).
- `app.asar.stock.bak` next to the live asar — `hermes-desktop-ru uninstall` swaps it back; `hermes update` for a full clone reset.
- MIT. Read `package/install.mjs` and `package/registry.json` if you want.

## Troubleshooting

| Symptom | What to do |
|---|---|
| "clone not found" | `--root` or `HERMES_AGENT_ROOT` |
| "packaged app.asar not found" | pack Desktop from the clone (`hermes desktop` / `npm run pack`). Website prebuilts are out of scope |
| Doctor FAIL | a critical file is gone — [issue "Doctor FAIL"](https://github.com/upmeister/hermes-desktop-ru/issues/new?template=doctor-fail.yml) |
| Doctor WARN / UI partly English | expected after a large Bots rewrite; wait for the next mod release or install as-is |
| Access denied / EBUSY | close Hermes Desktop and retry |
| macOS "app is damaged" / Gatekeeper | only self-built `.app` from the clone; do not patch the notarized website build |
| Long `npm ci` | normal with broken `node_modules` after `hermes update` (3–10 min) |
| UI partially English | `hermes-desktop-ru doctor`, then `install` and restart |
| Roll back the mod | `hermes-desktop-ru uninstall` (needs `.stock.bak` from a previous install). Or manually: close Desktop → replace `resources/app.asar` with `resources/app.asar.stock.bak` → launch; full reset — `hermes update` |

## Compatibility

| Hermes Desktop | |
|---|---|
| **0.20.5** | verified on Windows (doctor 865/865 at 1.2.0). A later Bots rewrite may WARN — install still proceeds |
| Linux / macOS | installer can resolve paths; **not author-tested**. Treat as experimental |
| older | install the mod release that matches |

Doctor FAIL after a fresh Hermes bump? That now means a critical *file* disappeared, not "Bots renamed a button". Open an [issue](https://github.com/upmeister/hermes-desktop-ru/issues/new/choose) or wait for the next mod release.

Upstream Desktop commits and new `en.ts` keys are logged in [UPSTREAM-WATCH.md](UPSTREAM-WATCH.md) (sensor + LLM note; releases stay manual).

## Glossary / what we do not translate

Proper names stay: platforms, models, providers, commands, theme names (`Midnight`, `Catppuccin`). Theme *descriptions* are translated.

Established terms stay: MCP, DIFF, URL, PR, YOLO.

Stable UI glossary: «Рабочие материалы» (Artifacts), «Обслуживание и диагностика» (Maintenance), «Рассуждения» (Reasoning).

Backend-produced text (CLI logs, tracebacks, JSON, OS messages) is not translated — it is not UI. Rare exceptions are patched when a backend string reaches the interface directly (e.g. the wake-word hint from `tui_gateway/server.py`).

## Credits

- [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru) — early translation base
- [anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru) — structural/doctor approach
- DrMaks22 — glossary and PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)

## License

[MIT](LICENSE)