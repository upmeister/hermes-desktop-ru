# 🇷🇺 Hermes Desktop — русский мод

[🇷🇺 Русский](README.md) · [🇬🇧 English](README.en.md)

Полная русская локализация [Hermes Desktop](https://github.com/NousResearch/hermes-agent).

[![Hermes Desktop](https://img.shields.io/badge/Hermes_Desktop-0.21.0-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![npm](https://img.shields.io/npm/v/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![npm](https://img.shields.io/npm/dm/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**Последний релиз: [v1.2.3](https://github.com/upmeister/hermes-desktop-ru/releases/tag/v1.2.3) · Hermes 0.21.0 · 2 сентября 2026**

Официальный клиент умеет несколько языков, но **русского в актуальной ветке нет**. Этот мод переводит весь UI — в том числе места, которые обычный файл локали не достаёт (Боты, канбан, подписи настроек, сообщения главного процесса). После `hermes update` ставится заново одной командой.

> Нужен Desktop **из исходников** (`hermes desktop` / `git clone`), не portable и не готовый установщик с сайта.
>
> **Windows** — основной путь. **Linux** — установщик прогнан автором (Ubuntu 26); после установки — `hermes desktop --skip-build`. Иконка в меню на Linux — баг апстрима, не мода. **macOS** — экспериментально, живого прогона нет. Официальный подписанный `.app` / AppImage с сайта **не патчим**.

| | Обычный locale pack | Этот мод |
|---|---|---|
| Каталог i18n (кнопки, настройки, онбординг) | да | да |
| Хардкоды в компонентах | нет | да |
| Боты, канбан, main-process | нет | да |
| После `hermes update` | часть строк снова на английском | `hermes-desktop-ru install` |

## Как выглядит

![Чат](docs/screenshots/chat.png)

![Настройки](docs/screenshots/settings.png)

![Боты и канбан](docs/screenshots/bots-kanban.png)

## Установка

Нужны Node.js 18+ и **закрытый** Hermes Desktop (сборка 5–10 минут).

Обычный путь клона:

- Windows: `%LOCALAPPDATA%\hermes\hermes-agent`
- Linux / macOS: `~/.hermes/hermes-agent`

```bash
npm install -g hermes-desktop-ru
hermes-desktop-ru install
```

| Команда | Что делает |
|---|---|
| `hermes-desktop-ru install` | установить / переустановить. Откатывает tracked-исходники клона к стоку |
| `hermes-desktop-ru doctor` | сухая проверка: ничего не пишет, процессы не убивает |
| `hermes-desktop-ru uninstall` | вернуть packaged `app.asar` из `.stock.bak` (клон не трогает) |
| `hermes-desktop-ru version` | версия пакета |
| `hermes-desktop-ru help` | справка |

Клон не там, где обычно:

```bash
hermes-desktop-ru install --root /path/to/hermes-agent
```

Подойдут и `HERMES_AGENT_ROOT`, и `HERMES_HOME`.

Без npm: скачайте [release zip](https://github.com/upmeister/hermes-desktop-ru/releases), распакуйте.

- Windows: `install.bat` (двойной клик) или `install.ps1`
- Linux / macOS: `./install.sh` или `node install.mjs` (нужен Node 18+ в PATH; если Desktop уже собирался, его Node часто лежит в `~/.hermes/node`)

Перед установкой Desktop должен быть хотя бы раз собран из этого клона (`hermes desktop` или `cd apps/desktop && npm run pack`). Установщик ищет `app.asar` только внутри `apps/desktop/release/` (`win-unpacked` / `win-arm64-unpacked` / `linux-unpacked` / `linux-arm64-unpacked` / `Hermes.app`).

После `УСТАНОВКА OK` запускайте Desktop через `hermes desktop --skip-build` (если язык не сменился сам — **Русский** в настройках). Не кликайте иконку сразу после установки: обычный `hermes desktop` пересобирает pack и затирает русский asar.

На Mac после подмены asar установщик ставит ad-hoc подпись. Это не нотаризация Apple: Gatekeeper может всё равно ругнуться. Если Desktop «повреждён» — вы не в том `.app` (нужен self-built из клона, не скачанный с сайта).

## После обновления Hermes

```text
hermes update  →  hermes-desktop-ru install  →  запуск Desktop
```

`hermes update` сам по себе **не** пересобирает уже установленный asar. Старый русский UI может «казаться живым» — это старый бандл. Всегда прогоняйте установщик.

Установщик сначала возвращает tracked-исходники клона к стоку. Если в том же клоне лежат другие ваши патчи — они не переживут установку. `doctor` этого не делает.

## Что переведено

| Область | Покрытие |
|---|---|
| i18n-каталог: чат, настройки, шлюз, биллинг, онбординг | ✅ полный |
| Хардкоды компонентов: поля настроек, splash, мессенджеры, темы | ✅ |
| Канбан, плагин Bots, сообщения main-процесса | ✅ |
| Реестр doctor (хардкод-якоря) | ✅ 720 правил |

## Конвенции перевода

- Имена собственные не трогаем: платформы, плагины, провайдеры, модели, команды, имена тем (`Midnight`, `Catppuccin`). Описания тем — переводим.
- Технические термины оставляем как есть: MCP, DIFF, URL, PR, YOLO, JSON.
- Устоявшиеся подписи UI: Artifacts → «Рабочие материалы», Maintenance → «Обслуживание и диагностика», Reasoning → «Рассуждения».
- Плюрализация — через `ruPlural`. Функциональные ключи английскими строками не подменяем (иначе краш «is not a function»).
- То, что приходит из бэкенда (логи, CLI, traceback, JSON, сообщения ОС), не переводим — технически перевести их без глубоких патчей бэкенда неосуществимо.
- Информация от внешних источников (провайдеры памяти вроде Honcho, сторонние сервисы, динамические схемы конфигурации) тоже не переводится — она прилетает извне и не является частью интерфейса мода.

Перед записью гоняется **doctor**: косметический пропуск или неоднозначный якорь (часто в Bots) оставит пятно по-английски — установка идёт. Остановка только если пропал файл критичного правила (канбан / connection-registry). Сборка (`npm run build`) — отдельный жёсткий стоп.

Актуальная совместимость и журнал апстрима — в [релизах](https://github.com/upmeister/hermes-desktop-ru/releases) и [UPSTREAM-WATCH.md](UPSTREAM-WATCH.md).

## Если что-то пошло не так

| Симптом | Что сделать |
|---|---|
| «не найден клон hermes-agent» | `--root` или `HERMES_AGENT_ROOT` |
| «не найден packaged app.asar» | соберите Desktop из клона (`hermes desktop` / `npm run pack`). Prebuilt с сайта не подойдёт |
| Doctor FAIL | пропал файл критичного правила — [issue](https://github.com/upmeister/hermes-desktop-ru/issues/new?template=doctor-fail.yml) |
| Doctor WARN, часть UI на английском | нормально после большого апдейта Bots; дождитесь следующего релиза мода или поставьте как есть |
| Linux: иконка в меню молчит, из терминала открывается | баг апстрима Hermes, не мод. Запуск: `hermes desktop --skip-build` |
| После мода UI снова английский / иконка крутится | `hermes desktop --skip-build`. Обычный запуск пересобирает pack и затирает asar |
| Access is denied / EBUSY / файл занят | закройте Desktop и шлюз, повторите |
| macOS: «приложение повреждено» / Gatekeeper | мод только для self-built `.app` из клона, не для скачанного с сайта |
| Долго на npm ci | нормально после `hermes update` (3–10 мин) |
| Часть UI на английском | `doctor`, затем `install`, перезапуск |
| Откатить мод | `hermes-desktop-ru uninstall` (нужен `.stock.bak` от прошлой установки). Или руками: закройте Desktop → замените `resources/app.asar` на `resources/app.asar.stock.bak` → запустите. Полный сброс клона — `hermes update` |

Баги и непереведённые места: [GitHub Issues](https://github.com/upmeister/hermes-desktop-ru/issues/new/choose).

Как это устроено технически (реестр якорей, doctor, asar) — в [английском README](README.en.md).

## Основа

- [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru) — ранняя база перевода
- [anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru) — идеи structural/doctor
- DrMaks22 — словарь и PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)

[MIT](LICENSE)
