# 🇷🇺 Hermes Desktop — русский мод

[🇷🇺 Русский](README.md) · [🇬🇧 English](README.en.md)

Полная русская локализация [Hermes Desktop](https://github.com/NousResearch/hermes-agent) для Windows.

[![Hermes Desktop](https://img.shields.io/badge/Hermes_Desktop-0.20.5-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![npm](https://img.shields.io/npm/v/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![npm](https://img.shields.io/npm/dm/hermes-desktop-ru?style=for-the-badge&color=red)](https://www.npmjs.com/package/hermes-desktop-ru)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**Последний релиз: [v1.0.4](https://github.com/upmeister/hermes-desktop-ru/releases/tag/v1.0.4) · Hermes 0.20.5 · 23 августа 2026**

Официальный клиент умеет несколько языков, но **русского в актуальной ветке нет**. Этот мод переводит весь UI — в том числе места, которые обычный файл локали не достаёт (Боты, канбан, подписи настроек, сообщения главного процесса). После `hermes update` ставится заново одной командой.

> Не для portable/prebuilt `.exe` — нужен Desktop, установленный из исходников (`git clone`).

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
Обычный путь клона: `%LOCALAPPDATA%\hermes\hermes-agent`

```powershell
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

```powershell
hermes-desktop-ru install -Root "D:\path\to\hermes-agent"
```

Без npm: скачайте [release zip](https://github.com/upmeister/hermes-desktop-ru/releases), распакуйте, запустите `install.bat`.

После `УСТАНОВКА OK` откройте Desktop (если язык не сменился сам — **Русский** в настройках).

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

Имена собственные и команды не трогаем; MCP, DIFF, URL, PR, YOLO — как есть.

Перед записью гоняется **doctor**: косметический пропуск оставит пятно по-английски, сдвиг логики — остановит установку.

Актуальная совместимость и журнал апстрима — в [релизах](https://github.com/upmeister/hermes-desktop-ru/releases) и [UPSTREAM-WATCH.md](UPSTREAM-WATCH.md).

## Если что-то пошло не так

| Симптом | Что сделать |
|---|---|
| «не найден клон hermes-agent» | `-Root` или `HERMES_AGENT_ROOT` |
| Doctor FAIL | апстрим ушёл вперёд — [issue](https://github.com/upmeister/hermes-desktop-ru/issues/new?template=doctor-fail.yml) |
| Access is denied / EBUSY | закройте Desktop и шлюз, повторите |
| Долго на npm ci | нормально после `hermes update` (3–10 мин) |
| Часть UI на английском | `doctor`, затем `install`, перезапуск |
| Откатить мод | `hermes-desktop-ru uninstall` (нужен `.stock.bak` от прошлой установки). Или руками: закройте Desktop → замените `resources\app.asar` на `resources\app.asar.stock.bak` → запустите. Полный сброс клона — `hermes update` |

Баги и непереведённые места: [GitHub Issues](https://github.com/upmeister/hermes-desktop-ru/issues/new/choose).

Как это устроено технически (реестр якорей, doctor, asar) — в [английском README](README.en.md).

## Основа

- [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru) — ранняя база перевода
- [anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru) — идеи structural/doctor
- DrMaks22 — словарь и PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)

[MIT](LICENSE)