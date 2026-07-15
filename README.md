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

## Лицензия

MIT
