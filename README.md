# 🇷🇺 Hermes Desktop — русский мод

Полная русская локализация [Hermes Desktop](https://github.com/NousResearch/hermes-agent) для Windows.

[![Hermes Desktop](https://img.shields.io/badge/Hermes_Desktop-0.20.5-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

![Hermes Desktop на русском](docs/screenshot.png)

> Единственный активно поддерживаемый русский мод для актуального Hermes Desktop.
> **100% покрытия UI** на 0.20.4 / 0.20.5: системные строки, настройки, канбан, Bots, фильтры сессий и хардкоды компонентов.
> После каждого обновления Hermes достаточно снова запустить установщик.

## Зачем этот мод

Официальный клиент уже умеет несколько языков, но **русского в актуальной ветке нет**.
Этот мод:

- переводит **весь** пользовательский интерфейс, а не только часть ключей;
- чинит строки, которые «не ловятся» обычным i18n (хардкоды в компонентах, Bots, поля настроек);
- **переживает `hermes update`**: после обновления клиента вы просто ставите мод заново;
- перед записью гоняет **doctor** — если апстрим слишком уехал, установщик честно остановится, а не сломает сборку.

## Установка

### Что нужно

1. Hermes Desktop, установленный **из исходников** (`git clone`), не portable/prebuilt `.exe`.
2. [Node.js](https://nodejs.org/) 18+ и npm.
3. Закрытый Hermes Desktop на время установки (5–10 минут на `npm run build`).

Стандартный путь клона:

```text
%LOCALAPPDATA%\hermes\hermes-agent
```

### Способ 1 — двойной клик

1. Скачайте [последний release zip](https://github.com/upmeister/hermes-desktop-ru/releases).
2. Распакуйте архив.
3. Запустите **`install.bat`**.

### Способ 2 — PowerShell

В папке с установщиком:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

Полезные флаги:

```powershell
# сухая проверка совместимости (ничего не меняет)
powershell -ExecutionPolicy Bypass -File install.ps1 -Doctor

# если клон лежит не в %LOCALAPPDATA%\hermes\hermes-agent
powershell -ExecutionPolicy Bypass -File install.ps1 -Root "D:\path\to\hermes-agent"

# справка
powershell -ExecutionPolicy Bypass -File install.ps1 -Help
```

Переменная окружения `HERMES_AGENT_ROOT` тоже задаёт путь к клону.

После `УСТАНОВКА OK` просто откройте Hermes Desktop — язык интерфейса станет русским
(при необходимости выберите **Русский** в настройках языка).

## После обновления Hermes

```text
hermes update  →  install.ps1 / install.bat  →  запуск Desktop
```

Установщик сам:

1. находит клон Hermes;
2. восстанавливает исходники к чистому стоку;
3. проверяет все якоря перевода (doctor);
4. применяет перевод;
5. пересобирает `dist` и упаковывает `app.asar`.

> Важно: сам `hermes update` **не** пересобирает уже установленный asar.
> Старый русский UI может «казаться живым» после апдейта, но это старый бандл.
> Надёжный путь — всегда прогонять установщик после обновления клиента.

## Что внутри

| Область | Покрытие |
|---|---|
| Основной i18n-каталог (чат, настройки, шлюз, биллинг, онбординг…) | 100% |
| Подписи и описания полей настроек | 100% |
| Канбан | 100% |
| Плагин Bots (агенты, группы, cron, petdex, хаб навыков, меню) | 100% |
| Фильтры/группировка сессий | 100% |
| Хардкоды UI (splash, мессенджеры, темы, MoA…) | 100% |

## Как переводим

- Имена собственные и команды **не трогаем** (платформы, модели, фильтры логов).
- Устоявшиеся термины оставляем: MCP, DIFF, URL, PR, YOLO.
- Единый словарь UI: «Рабочие материалы», «Обслуживание и диагностика», «Рассуждения».

## Совместимость

| Hermes Desktop | Статус |
|---|---|
| **0.20.5** | ✅ проверено (doctor 630/630, install OK) |
| **0.20.4** | ✅ 100% перевода |

Если doctor ругается после свежего апдейта Hermes — подождите релиз мода под новую версию
или откройте issue.

## Возможные проблемы

| Симптом | Что сделать |
|---|---|
| «не найден клон hermes-agent» | Укажите `-Root` или `HERMES_AGENT_ROOT` |
| Doctor FAIL | Апстрим ушёл вперёд — нужен новый релиз мода |
| Access is denied / EBUSY | Закройте Hermes Desktop и повторите |
| Долго на npm ci | Нормально при битых `node_modules` после `hermes update` (3–10 мин) |
| UI частично на английском | `-Doctor`, затем полная установка и перезапуск Desktop |
| `hermes update` и занятый `hermes.exe` | Это ограничение Windows, не мода: закройте Desktop/шлюз |

## Состав репозитория

```text
package/           установщик и движок (то, что попадает в release zip)
  install.bat      двойной клик
  install.ps1      CLI-обёртка
  install-asar.ps1 основной сценарий
  registry.json    630 структурных правил перевода
  files/           ru.ts + вспомогательные локали
i18n/              исходные локали для разработки
docs/screenshot.png
CHANGELOG.md
```

## Основа и благодарности

- [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru) — ранняя база перевода  
- [anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru) — идеи structural/doctor-подхода  
- DrMaks22 — словарь и PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)  

Спасибо авторам и сообществу Hermes ❤️

## Лицензия

[MIT](LICENSE)
