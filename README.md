# 🇷🇺 Hermes Desktop — Russian Language Mod

Полная русская локализация десктопного приложения [Hermes Agent](https://github.com/NousResearch/hermes-agent) (Windows).

[![Hermes Agent](https://img.shields.io/badge/Hermes_Agent-0.20.4+-FFD700?style=for-the-badge&logo=github)](https://github.com/NousResearch/hermes-agent)
[![Release](https://img.shields.io/github/v/release/upmeister/hermes-desktop-ru?style=for-the-badge&color=green)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![Downloads](https://img.shields.io/github/downloads/upmeister/hermes-desktop-ru/total?style=for-the-badge&color=orange)](https://github.com/upmeister/hermes-desktop-ru/releases)
[![License](https://img.shields.io/github/license/upmeister/hermes-desktop-ru?style=for-the-badge)](LICENSE)

**100% перевода**: весь i18n-каталог (defineLocale), настройки (`ru-constants`), канбан-плагин,
плагин **Bots целиком** (roster, групповые чаты, cron-задачи, профили, petdex, хаб навыков),
панель фильтров сессий, хардкоды компонентов (биллинг, MoA, уведомления, терминал, «Опасная зона», приветственное окно, мессенджеры).

## ⚡ Быстрый старт

1. Убедитесь, что Hermes установлен **из исходников** (`git clone`), а не prebuilt-`.exe` —
   путь по умолчанию `C:\Users\<you>\AppData\Local\hermes\hermes-agent`.
2. Закройте Hermes Desktop (установщик сам пересоберёт и перепакует приложение).
3. Скачайте [zip последнего релиза](https://github.com/upmeister/hermes-desktop-ru/releases),
   распакуйте и запустите:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

4. Запустите Hermes Desktop → интерфейс на русском.

> ⚠️ **Важно**: установщик собирает десктоп из клона (`npm run build`), это занимает 5–10 минут.
> Требуется [Node.js](https://nodejs.org/) 18+ и npm. При установке Hermes Desktop должен быть закрыт.

## 🔧 Методы установки

| Способ | Команда | Когда |
|---|---|---|
| **Установщик (рекомендуется)** | `powershell -ExecutionPolicy Bypass -File install.ps1` | Первая установка, после обновлений Hermes |
| **Доктор (диагностика)** | `powershell -ExecutionPolicy Bypass -File install.ps1 -Doctor` | Проверить, что все переводы лягут на текущий апстрим (без записи) |

Установщик автоматически:
1. Проверяет версию клона (`EXPECTED_COMMIT`, version-gate) — предупреждает при несовпадении;
2. Сбрасывает tracked-файлы к стоку (`git restore`) — untracked-локали не трогаются;
3. Прогоняет **doctor** (сухая проверка всех 630+ правил по якорям, блок при MISSING);
4. Применяет реестр якорей + структурный патчер i18n-регистрации;
5. Чинит `node_modules` при необходимости (deps-health → npm ci);
6. Собирает десктоп (`npm run build`) и перепаковывает `app.asar`.

## 🔄 Переживание обновлений Hermes

Мод построен на **структурном реестре якорей** (вариант C) вместо классического `git apply --3way`:

- Каждое правило — уникальный блок строк исходника (+ контекст/`all`-варианты);
- Движок `apply-hardcodes.mjs` ищет якорь по байтам, а не по хункам патча — поэтому
  переживает **реформат-коммиты апстрима** (`fmt(js): npm run fix` сломал все патчи 19.08, реестр — нет);
- Несовпадения не приводят к «молчаливому» пропуску: doctor пишет MISSING/AMBIGUOUS;
- `ru.ts` и другие файлы локалей — **untracked** в клоне: апдейт Hermes их не смывает,
  установщик восстанавливает их из `files/`.

После **каждого обновления Hermes** просто запустите install.ps1 заново (или `-Doctor`, чтобы убедиться).

## 📦 Состав релиза

```
hermes-desktop-ru/
├── i18n/
│   ├── ru.ts               # Перевод (defineLocale, весь интерфейс)
│   ├── ru-constants.ts     # Перевод fieldLabels/fieldDescriptions (настройки)
│   └── ru-locales.ts       # Перевод канбан-плагина
├── patches/
│   └── ru-mod-v3.patch     # Хардкоды компонентов (источник исторических правил)
├── package/
│   ├── install-asar.ps1    # Установщик v7 (version-gate → restore → doctor → apply → build → asar)
│   ├── install.bat         # Обёртка для двойного клика
│   ├── registry.json       # Реестр якорей (630+ правил: патч + overrides)
│   ├── overrides.json      # Ручной слой правил (новые хардкоды)
│   ├── apply-hardcodes.mjs # Движок application (apply/--doctor, идемпотентный)
│   ├── gen-registry.mjs    # Генератор реестра из патча + overrides
│   ├── structural-i18n.mjs # Патчер i18n-регистрации по структурным якорям
│   ├── deps-health.mjs     # Проверка node_modules (npm ci при битых)
│   ├── EXPECTED_COMMIT     # Коммит апстрима, на котором собран мод
│   └── files/              # untracked-локали (ru.ts, ru-constants, ru-locales)
└── README.md
```

## ✨ Что переведено

| Область | Статус |
|---|---|
| **i18n-каталог** (весь интерфейс: чат, настройки, биллинг, MCP, шлюз, клавиатура, онбординг…) | ✅ 100% |
| **Поля настроек** (`ru-constants.ts`, ~100 ключей RU_FIELD_LABELS/DESCRIPTIONS) | ✅ |
| **Канбан-плагин** (`ru-locales.ts`, 190+ ключей) | ✅ |
| **Bots-плагин** (roster, групповые чаты, cron-задачи, petdex, хаб навыков, райтклик-меню, поповеры) | ✅ 100% |
| **Панель фильтров сессий** (Grouping/Ordering/Show/Status/PR/Archived…) | ✅ |
| **Хардкоды компонентов** (биллинг, МоA, custom-endpoints, приветственное окно, «Подключение…», «Это устройство», мессенджеры, уталки, 28 описаний провайдеров, 6+ тем) | ✅ |
| **Функциональные ключи EN** (плейсхолдеры с `${}`, плюрализация) | ✅ переведены без потери логики |

## 📐 Конвенции перевода

- **Имена собственные** (платформы, плагины, провайдеры, модели, команды, лог-фильтры) — не переводим;
- **Технические термины** (MCP, DIFF, URL, PR, Pull request) — остаются в оригинале;
- «Артефакты» → «Рабочие материалы», Maintenance → «Обслуживание и диагностика»;
- `model.reasoning` = «Рассуждения» (единый термин);
- cron-терминология унифицирована с основным клиентом («Новая cron-задача»);
- Плюрализация — через `ruPlural(n, 'одна', 'неск', 'много')`;
- **Функциональные ключи EN нельзя заменять строками** — краш «is not a function»
  (инцидент 16.08; аудит типов — при каждой волне перевода).

## 🩺 Возможные проблемы

| Проблема | Решение |
|---|---|
| Doctor показывает MISSING/AMBIGUOUS | Апстрим сильно изменился — обновите мод до свежего релиза (EXPECTED_COMMIT) |
| «Access is denied» при сборке | Hermes Desktop запущен — закройте и повторите |
| Сборка падает на diff-маркерах | В клоне остались артефакты прошлых модов — установщик сам делает `git restore`, либо `git checkout .` вручную |
| Electron не скачивается (сеть) | `ELECTRON_MIRROR=<mirror> hermes desktop --force-build` |
| Интерфейс частично английский | Запустите `-Doctor` и перезапустите Desktop (старый бандл в памяти) |
| Обновление Hermes не пускает (hermes.exe locked) | Это не связано с модом: закройте Desktop/шлюз/другие REPL и повторите `hermes update` |

## ↔️ Совместимость

| Hermes (коммит) | Мод |
|---|---|
| 0.20.4+ / `f43eabee5f` (08.2026) | v7.x, реестр 630+ правил |
| 0.20.4 / `2d92793045` | v7.0 (реестр 399) |

При выходе новой версии Hermes — запустите `install.ps1 -Doctor`: реестр якорей сообщит,
пережил ли он апстрим; если нет — дождитесь обновления мода.

## 📜 Основа перевода

Базовый перевод — из [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru)
(конвертирован в `defineLocale`), использованы наработки
[anatolijlaptev1991-ctrl/hermes-ru](https://github.com/anatolijlaptev1991-ctrl/hermes-ru)
(структурные якоря, patch-engine, контрактные тесты; часть идей), diff-словарь DrMaks22
(PR [#72250](https://github.com/NousResearch/hermes-agent/pull/72250)), плюс собственные
волны перевода (v3.x → v7.x) и сверка спорных терминов с реальными переводами.

Спасибо авторам этих проектов за базу и идеи! ❤️

## 📄 Лицензия

MIT — делайте что хотите, ссылка на автора приветствуется.