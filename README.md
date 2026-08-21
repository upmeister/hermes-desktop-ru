# 🇷🇺 Hermes Desktop — Russian Language Mod

Полная русская локализация десктопного приложения [Hermes Agent](https://github.com/NousResearch/hermes-agent) (Windows).

[![Hermes Agent](https://img.shields.io/badge/Hermes_Agent-0.20.4-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License](https://img.shields.io/github/license/upmeister/hermes-desktop-ru?style=for-the-badge)](LICENSE)

![Hermes Desktop на русском](docs/screenshot.png)

**Реальные 100% перевода** для клиента **Hermes Desktop 0.20.4** (проверен и на 0.20.5):
весь i18n-каталог, поля настроек, канбан-плагин, плагин **Bots целиком** (roster, групповые чаты,
cron-задачи, профили, petdex, хаб навыков), панель фильтров сессий и хардкоды компонентов
(биллинг, MoA, custom endpoints, приветственное окно, «Это устройство», мессенджеры и другое).

## ⚡ Быстрый старт

1. Hermes должен быть установлен **из исходников** (`git clone`), а не prebuilt-`.exe` —
   стандартный путь: `C:\Users\<you>\AppData\Local\hermes\hermes-agent`.
2. Закройте Hermes Desktop (установщик сам пересоберёт и перепакует приложение).
3. Скачайте [zip последнего релиза](https://github.com/upmeister/hermes-desktop-ru/releases),
   распакуйте и выполните:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

4. Запустите Hermes Desktop — интерфейс на русском.

> ⚠️ Установщик собирает десктоп из клона (`npm run build`, 5–10 минут). Требуются
> [Node.js](https://nodejs.org/) 18+ и npm. При установке Hermes Desktop должен быть закрыт.

## 🔁 После обновлений Hermes

Просто запустите установщик заново — он сам сбросит исходники к актуальному стоку,
проверит совместимость всех переводов и пересоберёт приложение. Дополнительно можно
сделать сухую проверку без записи:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -Doctor
```

## ✨ Что переведено

| Область | Статус |
|---|---|
| **i18n-каталог** (весь интерфейс: чат, настройки, биллинг, MCP, шлюз, клавиатура, онбординг…) | ✅ 100% |
| **Поля настроек** (названия и описания полей) | ✅ |
| **Канбан-плагин** | ✅ 100% |
| **Bots-плагин** (roster, групповые чаты, cron-задачи, petdex, хаб навыков, меню) | ✅ 100% |
| **Панель фильтров сессий** (группировка, сортировка, статусы, архив…) | ✅ |
| **Хардкоды компонентов** (биллинг, MoA, custom endpoints, приветственное окно, «Подключение…», «Это устройство», мессенджеры, описания провайдеров, темы) | ✅ |
| **Функциональные ключи** (плейсхолдеры, плюрализация) | ✅ переведены без потери логики |

## 📐 Конвенции перевода

- **Имена собственные** (платформы, плагины, провайдеры, модели, команды, лог-фильтры) — не переводим;
- **Технические термины** (MCP, DIFF, URL, PR, Pull request) — остаются как есть;
- «Артефакты» → «Рабочие материалы», Maintenance → «Обслуживание и диагностика»;
- единая терминология: «Рассуждения», «cron-задача» (как в основном клиенте).

## 🩺 Возможные проблемы

| Проблема | Решение |
|---|---|
| Doctor сообщает о несовпадении | Апстрим сильно изменился — скачайте актуальный релиз мода |
| «Access is denied» при сборке | Hermes Desktop запущен — закройте и повторите |
| Сборка падает на diff-маркерах | В клоне остались артефакты прошлых модов — установщик сам делает сброс (`git restore`), либо выполните `git checkout .` вручную |
| Electron не скачивается (сеть) | `ELECTRON_MIRROR=<mirror> hermes desktop --force-build` |
| Интерфейс частично английский | Сделайте `-Doctor`, перезапустите установку и Hermes Desktop |
| `hermes update` ругается на занятый hermes.exe | Это не связано с модом: закройте Desktop/шлюз/другие REPL и повторите обновление |

## ↔️ Совместимость

| Hermes | Мод |
|---|---|
| 0.20.5 / `2584b7c4` (08.2026) | ✅ проверен (doctor 630/630, install OK) |
| 0.20.4 (08.2026) | ✅ реальные 100% перевода |

## 👤 Об авторе

Мод поддерживается **активным пользователем и участником сообщества Hermes**.
Перевод регулярно обновляется по мере выхода новых версий клиента — следите за
[релизами](https://github.com/upmeister/hermes-desktop-ru/releases).

## 📜 Основа перевода

Базовый перевод — из [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru)
(конвертирован в `defineLocale`); использованы наработки
[anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru)
и дифф-словарь DrMaks22 (PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)),
плюс собственные волны перевода и сверка спорных терминов.

Спасибо авторам этих проектов за базу и идеи! ❤️

## 📄 Лицензия

MIT — делайте что хотите, ссылка на автора приветствуется.