# Hermes Desktop — Russian Language Mod (Русский мод)

Добавляет русский язык интерфейса в десктопное приложение Hermes Agent.

## Как это работает

Мод использует встроенную систему i18n Hermes Desktop: функцию `defineLocale()` из `apps/desktop/src/i18n/define-locale.ts`. Она создаёт **частичный** перевод — все ключи, которых нет в `ru.ts`, автоматически берутся из английского оригинала (`en.ts`). Это значит:

- Интерфейс не ломается при обновлении Hermes (новые ключи просто будут на английском)
- Не нужно переводить 100% строк — только те, что реально используются
- `defineLocale()` глубоко сливает русские переводы поверх английской базы

## Состав мода

```
desktop-ru-mod/
├── i18n/
│   ├── ru.ts              # Перевод (defineLocale, частичный)
│   ├── ru-constants.ts    # Перевод fieldLabels/fieldDescriptions
│   ├── types.ts           # Добавлен 'ru' в тип Locale
│   ├── languages.ts       # Добавлен русский в список языков
│   └── catalog.ts         # Добавлен импорт ru в TRANSLATIONS
├── scripts/
│   ├── patch-components.py # Патч компонентов настроек
│   └── patch-skills.py    # Патч описаний навыков
├── rebuild.sh             # Скрипт пересборки после обновления
├── launch-hermes-ru.bat   # Лаунчер (Windows) с env-переменными
└── .gitignore
```

## Установка

```bash
# Клонировать мод в ~/.hermes/desktop-ru-mod/
git clone https://github.com/upmeister/hermes-desktop-ru.git ~/.hermes/desktop-ru-mod

# Запустить сборку
bash ~/.hermes/desktop-ru-mod/rebuild.sh

# Перезапустить Hermes Desktop
```

## После обновления Hermes

```bash
bash ~/.hermes/desktop-ru-mod/rebuild.sh
```

Скрипт скопирует файлы мода в исходники, пересоберёт фронтенд и обновит dist.

## Как переводить новые ключи

1. Сравни `ru.ts` с `en.ts` (в `apps/desktop/src/i18n/`)
2. Добавь недостающие ключи в `ru.ts` в том же формате
3. `npm run build` в `apps/desktop/`
4. Проверь: `grep "твой-перевод" dist/assets/index-*.js`

## Основа перевода

Базовый перевод взят из [warment/hermes-desktop-ru](https://github.com/warment/hermes-desktop-ru) (1782 строки), сконвертирован в формат `defineLocale()` для автоматического fallback на английский.

## Установка (правило v2, 13.08.2026)

**НЕ ставить пакетный dist** — он затирает другие моды клона (урок 13.08: v1 затёр ru-мод).
База установки — ВСЕГДА свежий `npm run build` из клона Windows (включает ВСЕ патчи клона:
ru + timestamps + будущие):

1. Клон на месте: `C:\Users\covhnw\AppData\Local\hermes\hermes-agent`
2. Запустить `package\install.bat` (или `install-asar.ps1` напрямую):
   - шаг 1: `npm run build` в `apps\desktop` (vite + bundle-electron-main + stage-native-deps)
   - шаг 2: пересборка `app.asar` (extract со stubs → replace `dist/` → `pack --unpack "**"`)
   - бэкап: `app.asar.stock.bak` рядом
3. Перезапустить Hermes Desktop.

Пакетный `dist/` в этом репо — только fallback при упавшей сборке (не основной путь).

## Состав (актуальный, 12.08.2026)

- `i18n/` — финальные локали из прода: en.ts, types.ts, ru.ts, zh.ts, ru-constants.ts,
  custom-endpoints-settings.tsx, ru-locales-kanban.ts (перевод канбан-плагина)
- `patches/` — ru-mod-v3.patch (i18n-пересборка под апстрим 76d832d38: 4 файла),
  desktop-timestamps-mod.patch (3 файла рендерера)
- `package/` — install.bat + install-asar.ps1 (v2, правило выше)
- Корень — инструменты перевода (merge/dedup/fix-скрипты), история работы

## Лицензия

MIT
