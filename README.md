# Hermes Desktop — Russian Language Mod (Русский мод)

Русская локализация десктопного приложения [Hermes Agent](https://github.com/NousResearch/hermes-agent).
Работает на **0.20.4** (проверено; механизм структурных якорей рассчитан на будущие версии).
Покрытие: **97% ключей i18n** (2912 из 2855 EN + свои), плюс перевод канбан-плагина, настроек,
плагинов и хардкодов (терминал, «Опасная зона», таймстампы — см. ниже).

## Как это работает

Мод использует встроенную i18n системы Hermes Desktop — `defineLocale(overrides)` из
`apps/desktop/src/i18n/define-locale.ts`. Это **глубокий merge поверх EN**:
- ключей, которых нет в `ru.ts`, — fallback на английский → интерфейс не ломается при апдейтах;
- но **функциональные ключи EN (плейсхолдеры, плюрализация) нельзя заменять строками** — иначе
  `r.titlebar.layoutEditorTitle is not a function` (краш рендерера, инцидент 16.08). См. «Как переводить».

Регистрация русской локали (`ru` в `types.ts`, `catalog.ts`, `languages.ts`) выполняется
**структурным патчером по якорям**, а не хунками патча — поэтому переживает рефакторинг апстрима
(0.20.4 переписал `catalog.ts`, и старые хунки потеряли `ru` → ru=no → весь UI на английском).

## Состав мода (v5, 16.08.2026)

```
hermes-desktop-ru/
├── i18n/
│   ├── ru.ts               # Перевод (defineLocale, ~97% покрытия)
│   ├── ru-constants.ts     # Перевод fieldLabels/fieldDescriptions (настройки)
│   └── ru-locales.ts       # Перевод канбан-плагина (167+8 notify-ключей)
├── patches/
│   └── ru-mod-v3.patch     # Хардкоды компонентов (12 файлов, БЕЗ i18n/ — их шьёт патчер)
├── package/
│   ├── install-asar.ps1    # Установщик (restore → structural-i18n → build → asar)
│   ├── structural-i18n.mjs # Патчер i18n-регистрации по структурным якорям (идемпотентный)
│   ├── files/ru.ts, ru-constants.ts, ru-locales.ts   # untracked-файлы мода (переживают апдейты)
│   └── install.bat         # Обёртка для установщика
└── README.md
```

## Установка (Windows)

> База — ВСЕГДА свежий `npm run build` из клона Windows (включает ВСЕ патчи клона).
> **Никогда** не ставить пакетный dist — он затирает другие моды клона.

1. Клон на месте: `C:\Users\covhnw\AppData\Local\hermes\hermes-agent`
2. Запустить `package\install.bat` (или `install-asar.ps1` напрямую):
   - `git apply` патча `patches\ru-mod-v3.patch` (хардкоды, если ещё не применён);
   - восстановить untracked-файлы из `files\` (ru.ts, ru-constants, ru-locales);
   - **`node structural-i18n.mjs`** → добавляет `ru` в `types/catalog/languages` по якорям
     (идемпотентно, безопасно на стоковом апстриме);
   - `npm run build` в `apps\desktop`;
   - пересборка `app.asar` (extract со stubs → replace `dist/` → `pack --unpack "**"`)
     + бэкап `app.asar.stock.bak`.
3. Перезапустить Hermes Desktop.

## После обновления Hermes

Просто повторить шаг 2 — установщик сам смоет старый мод в клоне и пересоберёт.
Untracked-файлы (`files/`) переживают апдейты (проверено на 0.20.1); tracked-хунки патча
установщик восстанавливает повторным `git apply`; а каталожную регистрацию `ru` всегда
делает структурный патчер — даже если апстрим её перепишет.

Проверка после установки: бандл должен содержать маркеры — `findstr "Применить" <путь>\dist\assets\*.js`
(или открыть Настройки → верхняя строка должна быть на русском).

## Как переводить новые ключи

1. Сверь `ru.ts` с `en.ts` (`apps/desktop/src/i18n/`). Проверь **все** ключи по типам:
   - `EN` — значение-функция (например `mod => \`...${mod}...\``)? → в `ru.ts` тоже функция
     с теми же параметрами, **не строка** (иначе краш «is not a function»).
   - `EN` — строка? → переводи как строку.
2. Допиши в `ru.ts` в том же формате; для плюрализации используют `ruPlural(n, 'одна', 'неск', 'много')`.
3. Прогони синтаксис: `npx -p typescript@5.9.2 tsc --noEmit --noResolve --skipLibCheck --target es2022
   --module esnext --moduleResolution bundler --jsx react-jsx i18n/ru.ts` (только твои ошибки;
   нерезолвные импорты `@/...` — норма в изоляции).
4. Регистрацию новых категорий (если секции нет в EN) не трогать — fallback на EN.
5. `npm run build` в `apps\desktop`, проверь сборку и маркер в `dist/assets/`.

Совет: при добавлении новых ключей пользуйся аудитом типов — сравнение en/ru в рантайме
(конвертация в .mjs + walk) ловит все «EN=функция, RU=строка» разом. Утилиты — `~/projects/hermes-desktop-ru/tools/` (исторически в `/tmp/ts2mjs`).

## Таймстампы

Апстрим 0.20.4 ввёл **нативные таймстампы** (компонент `MessageTimelineTimestamp`, гейт
`display.timestamps` в `~/.hermes/config.yaml`, выключены по умолчанию). Включаются:
`hermes config set display.timestamps true`. Свой таймстамп-мод удалён (был несовместим с 0.20.4).
Дизайн нативных задаётся Tailwind-классами (`data-slot="timeline-timestamp"`,
`text-[0.625rem] … text-muted-foreground/55`) — при желании можно перекрыть CSS-оверрайдом в своём
стиле (без пересборки, точечно).

## История ключевых версий

- **v3.12.1 (16.08)** — фикс краша: 3 функциональных ключа EN (layoutEditorTitle/mcpSuggestions.tip/
  commitPlaceholder) вернули к функции. **v3.12** — перевод 108 новых ключей 0.20.4 (Connections,
  MCP deep-links, update-blocker, appearance, kanban-notify), ре-регистрация `ru` (0.20.4 переписал catalog.ts).
- **v5 установщика (16.08)** — структурный патчер i18n по якорям (+ doctor-проверка состояния).

## Основа перевода

Базовый перевод — из [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru)
(конвертирован в `defineLocale`), diff-словарь DrMaks22 (PR #72250), плюс собственные волны перевода
(4 + 4.1 + 4.2 x 10 опросников, 5.1 = 108 новых ключей). Сверка спорных технических терминов —
с реальными переводами в интернете и каталогом терминов.

## Лицензия

MIT
