# 🇷🇺 Hermes Desktop — Russian mod (English)

[🇬🇧 English](README.en.md) · [🇷🇺 Русский](README.md)

Full Russian localization for [Hermes Desktop](https://github.com/NousResearch/hermes-agent) on Windows.

[![Hermes Desktop](https://img.shields.io/badge/Hermes_Desktop-0.20.5-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![npm](https://img.shields.io/npm/v/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![npm](https://img.shields.io/npm/dm/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

![Hermes Desktop in Russian](docs/screenshot.png)

> The only actively maintained Russian mod for the current Hermes Desktop.
> **100% UI coverage** on **0.20.5** (doctor 642/642): system strings, settings,
> kanban, Bots, session filters — and hardcoded component strings that i18n
> can't reach.
> Upstream Hermes is tracked by an AI agent 24/7 and promptly re-translated —
> see the [watch log](UPSTREAM-WATCH.md). After `hermes update`, just re-run the installer.

## The problem

Hermes Desktop has **no Russian locale in the current release line** (upstream
`ru` PRs have been open since July without movement). Generic i18n-only locale
packs translate the catalog but leave dozens of **hardcoded strings** in
components, settings field labels, Bots and kanban plugin surfaces, and
main-process messages — still English.

## What makes this mod different

| Approach | Catalog keys | Hardcoded strings | Bots/Kanban | Main-process |
|---|---|---|---|---|
| i18n-only locale pack | ✅ (~2200 keys) | ❌ | ❌ | ❌ |
| **this mod** | ✅ (full catalog) | ✅ | ✅ | ✅ |

- **642-rule structural registry** patches hardcoded strings directly in the
  sources (renderer components, `ru-constants.ts` field labels, Bots plugin,
  kanban plugin i18n, Electron main-process messages).
- **Doctor-gated installer** — dry-run compatibility check before anything is
  written; cosmetic misses warn, critical drift fails loudly (no silent half-applied state).
- **Survives `hermes update`**: after updating the client, just re-run the
  installer. One command, ~5–10 min rebuild.
- **Regularly updated** for new Hermes features — watch the [releases](https://github.com/upmeister/hermes-desktop-ru/releases).

## Why structural anchors instead of git patches

`git apply --3way` on a shallow clone can **lie**: it exits 0 while leaving
`<<<<<<<` conflict markers in working files, and the build then dies with
"Encountered diff marker" — invisibly, and the markers break the *next* mod
too. The registry instead:

- matches **full unique string blocks** (`before` → `after`) anywhere in the file — survives upstream shifts/inserts;
- is **idempotent** and EOL-preserving;
- reports `MISSING`/`AMBIGUOUS` rules explicitly (exit 1) instead of silently skipping;
- `EXPECTED_COMMIT` version gate warns (does not block) when upstream moves past the build base.

The installer always: restores tracked sources to stock → runs doctor →
applies registry rules → registers the `ru` locale (catalog/languages/types) →
copies locale files → rebuilds `dist` → repacks `app.asar` (original kept as
`.stock.bak`).

## Installation

### Requirements

1. Hermes Desktop installed **from source** (`git clone`), not a portable/prebuilt `.exe`.
2. [Node.js](https://nodejs.org/) 18+ and npm.
3. Hermes Desktop closed during install (5–10 min `npm run build`).

Standard clone path: `%LOCALAPPDATA%\hermes\hermes-agent`

### npm (recommended)

```powershell
npm install -g hermes-desktop-ru
hermes-desktop-ru install
```

| Command | What it does |
|---|---|
| `hermes-desktop-ru install` | install / re-install the mod |
| `hermes-desktop-ru doctor` | dry-run compatibility check |
| `hermes-desktop-ru help` | help |

Non-standard clone location:

```powershell
hermes-desktop-ru install -Root "D:\path\to\hermes-agent"
```

(`HERMES_AGENT_ROOT` env var works too.)

### Without npm

Download the [latest release zip](https://github.com/upmeister/hermes-desktop-ru/releases),
unpack and run **`install.bat`** (or `install.ps1` / `install.ps1 -Doctor` / `-Root …`).

After `УСТАНОВКА OK` open Hermes Desktop — the UI is Russian
(if needed, pick **Русский** in the language settings).

## After updating Hermes

```text
hermes update  →  hermes-desktop-ru install  →  launch Desktop
```

The installer locates the clone, restores sources to stock, runs doctor,
applies translations, rebuilds `dist` and repacks `app.asar`.

> Note: `hermes update` does **not** rebuild the already-installed asar.
> The old Russian bundle may "look alive" after an update — that's the stale
> bundle. Always re-run the installer after updating the client.

## Doctor

`hermes-desktop-ru doctor` is a dry run (nothing is written). It reports:

- `OK` — every registry rule matches the current clone;
- `WARN` — cosmetic rules missing (that spot stays English, install proceeds);
- `FAIL` — critical drift (logic moved): install stops with a clear reason.

## Compatibility

| Hermes Desktop | Status |
|---|---|
| **0.20.5** | ✅ verified (doctor 642/642, install OK) |
| below 0.20.5 | ⚠️ older checks; install the mod matching your version |

Doctor complains after a fresh Hermes update? Wait for the next mod release or
[open an issue](https://github.com/upmeister/hermes-desktop-ru/issues/new/choose).

## Safety

- Everything runs **locally**: no backend, no telemetry, no network calls.
- Doctor gate before any write; tracked sources are restored to stock first.
- `app.asar` is backed up (`.stock.bak`) — a stock install can be restored.
- Open source, MIT — review the installer yourself (`package/install-asar.ps1`,
  `package/registry.json`).

## Troubleshooting

| Symptom | What to do |
|---|---|
| "clone not found" | `-Root` or `HERMES_AGENT_ROOT` |
| Doctor FAIL | upstream moved ahead — [issue "Doctor FAIL"](https://github.com/upmeister/hermes-desktop-ru/issues/new?template=doctor-fail.yml) |
| Access denied / EBUSY | close Hermes Desktop and retry |
| Long `npm ci` | normal with broken `node_modules` after `hermes update` (3–10 min) |
| UI partially English | `hermes-desktop-ru doctor`, then `install` and restart |
| Roll back the mod | close Desktop → replace `resources\app.asar` with `resources\app.asar.stock.bak` (kept by the installer next to it) → launch; full reset — `hermes update` |
| `hermes update` and busy `hermes.exe` | Windows limitation: close Desktop/gateway |

## What we translate (and what we don't)

- Proper names and commands stay untranslated: platforms, models, providers, log filters.
- Established terms are kept: MCP, DIFF, URL, PR, YOLO.
- Consistent glossary: «Рабочие материалы» (Artifacts), «Обслуживание и диагностика» (Maintenance), «Рассуждения» (Reasoning).

## Credits

- [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru) — early translation base
- [anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru) — structural/doctor approach ideas
- DrMaks22 — glossary and PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)

Thanks to the authors and the Hermes community ❤️

## Upstream watch

[UPSTREAM-WATCH.md](UPSTREAM-WATCH.md) — automated log of Hermes releases and
Desktop commits (maintained by an AI agent around the clock): new versions,
new i18n keys, what to verify before the next mod release.

## Feedback

Bugs, untranslated spots, doctor failures — via
[GitHub Issues](https://github.com/upmeister/hermes-desktop-ru/issues/new/choose)
(templates available): version, doctor output and a screenshot in one place.

## License

[MIT](LICENSE)