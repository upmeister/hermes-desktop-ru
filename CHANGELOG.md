# Changelog

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).
Версии мода не совпадают 1:1 с версиями Hermes Desktop.

## [Unreleased]

## [7.6.1] - 2026-08-22

### Fixed
- Установщик больше не хардкодит домашний путь автора: автопоиск клона через
  `%LOCALAPPDATA%\hermes\hermes-agent`, `HERMES_AGENT_ROOT` и флаг `-Root`.
- Release-zip снова кладёт локали в `files/` (как ждёт установщик) и включает `probe-ru.mjs`.
- Плоский zip (файлы в корне) тоже принимается — fallback по имени файла.
- Русские статусы установщика + `-Help` / `install.bat -Help`.

### Changed
- README переписан под конечного пользователя (установка через `.bat` и `.ps1`).
- Новый скриншот в шапке README (нейтральные названия сессий).

## [7.6.0] - 2026-08-21

### Added
- Первый публичный GitHub Release (`hermes-desktop-ru-v7.6.zip`).
- Реестр **630** структурных якорей (вариант C) вместо `git apply --3way`.
- Полный перевод плагина Bots, панели фильтров сессий, полей New Agent / Edit Profile / cron.
- `install.ps1` как user-facing обёртка; `deps-health.mjs` с workspace-резолвом
  (`@rolldown/plugin-babel` и другие nested deps).
- Doctor (`-Doctor`), version-gate (`EXPECTED_COMMIT`), auto `npm ci` при битых node_modules.
- MIT license, topics, user-facing README.

### Fixed
- Ложный `missing: @rolldown/plugin-babel` после `npm ci` (workspace hoisting).
- Рассинхрон `package/files/ru.ts` ↔ `i18n/ru.ts` (Intro Splash, «Рассуждения»).

### Compatibility
- Hermes Desktop **0.20.5** (`2584b7c4`) — doctor 630/630, install OK.
- Hermes Desktop **0.20.4** — 100% UI.

## [7.5.0] - 2026-08-21

### Added
- Лейблы полей New Agent / Edit Profile / cron (Имя, Заголовок, Провайдер, Модель…).
- SOUL.md label/placeholder, help-тексты про общий OAuth.

## [7.4.0] - 2026-08-21

### Added
- Advanced-поля «Новый агент», вкладки Общие/Возможности/Дополнительно.
- Панель фильтров сессий (`filter-menu.tsx`).
- Унификация термина «cron-задача».

## [7.2.0] – [7.3.0] - 2026-08-20

### Added
- Полный перевод плагина Bots (roster, group chats, cronjobs, petdex, skills hub).

## [7.1.0] - 2026-08-20

### Added
- Переживание апстрим-реформата (`fmt(js)`): doctor 399/399 на новом HEAD.
- Описания новых тем, вкладки «Сессии»/«Канбан», Intro Splash, «Рассуждения».

## [7.0.0] - 2026-08-20

### Changed
- **Вариант C**: `git apply --3way` заменён на structural registry engine
  (`apply-hardcodes.mjs` + `registry.json` + `overrides.json`).
- Установщик v7: restore → doctor → apply → structural-i18n → build → asar.

### Fixed
- Root-cause крашей «Encountered diff marker» на shallow-клоне после апдейта.
