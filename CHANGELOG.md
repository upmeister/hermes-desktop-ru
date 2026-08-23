# Changelog

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).
Версии мода не совпадают 1:1 с версиями Hermes Desktop.

> Нумерация начата с 1.0.0 — это первый стабильный публичный релиз.
> Предыдущая линия 7.6.x (август 2026) считается тестовой и здесь не описывается;
> её историю можно посмотреть в git-истории репозитория.

## [Unreleased]

## [1.0.5] - 2026-08-23

### Fixed
- Тосты плагина Bots: «Could not open `<имя>`'s chat — try again» → «Не удалось
  открыть чат `<имя>` — попробуйте ещё раз» (2 правила на `hermes-bots/plugin.js`).
- Тосты реакций: «Could not react» / «No active session» / «Gateway not connected»
  (`store/reactions.ts` + `api/client.ts` `notConnectedErrorMessage`).
- `updates`-секция ru.ts: стадия `error` — «Обновление приостановлено» (было
  «ошибка»); `applyingBody` (была старая английская), `applyingBodyBackend` и
  `guiSkewBody` (были пустые) — переведены; добавлены 7 недостающих ключей
  (`clientAlsoBehind*`, `everything*`).

### Changed
- Скриншот «Боты и канбан» в обоих README заменён (1280px).
- `*.tgz` добавлен в `.gitignore` (артефакт `npm pack` убран из git).
- Registry: 642 → 647 правил.

## [1.0.4] - 2026-08-23

### Added
- Сухой doctor: не убивает процессы, не делает `git restore`, не запускает `npm ci`;
  при грязном дереве — WARN и проверка текущего дерева.
- `hermes-desktop-ru uninstall` / `-Uninstall`: откат packaged `app.asar` из
  `.stock.bak` (+ `dist.stock.bak`), клон не трогается.
- `hermes-desktop-ru version` / `-Version`: версия пакета из `package.json`.
- `-AllowStaleDist`: явный флаг вместо тихого fallback на `package/dist`.
- CI: `.github/workflows/check.yml` (`node --check` + parse `registry.json`).
- Перевод «Send Diagnostics» (секция `sendDiagnostics`): загрузка отладочного
  пакета в поддержку Nous (новая фича апстрима) — title, privacy notice, статусы,
  ссылки поддержки.
- README: русский юзер-френдли + английский инженерный (structural anchors,
  doctor, safety, troubleshooting, глоссарий), таблица покрытия,
  3 скриншота (чат / настройки / боты+канбан).

### Changed
- Установщик шире гасит процессы: не только `Hermes`, но и процессы с Path
  внутри клона.
- `build-release-zip.py`: рассинхрон `i18n/ru.ts` vs `package/files/ru.ts` —
  теперь `exit 1` (раньше WARN).
- `gen-registry.mjs`: `let rules` — `override.delete` больше не падает.
- `EXPECTED_COMMIT` → `987064caa4f` (актуальный апстрим на момент релиза).

## [1.0.3] - 2026-08-22

### Added
- Перевод новых настроек «Внешний вид» из апстрима `14c59f0b505`: «Полоса вкладок»
  (`tabStripTitle/Desc/Auto/Always/Never`).

## [1.0.2] - 2026-08-22

### Fixed
- Doctor больше не блокирует установку из-за косметических пропусков: добавлено
  severity-ранжирование правил. Поведенческие (insert-after: `connection-registry.ts-2`,
  `plugin.tsx-1`) помечены `critical`; пропуск 1–2 критичных → WARN + установка
  продолжается, ≥3 → FAIL. Косметические пропуски (текст) установку никогда не
  блокируют — в итоге отчёт «переведено X из Y».
- Удалено устаревшее правило `hermes-bots-Bot_Chat` (апстрим перешёл на
  каноническое имя «Bot Chat» — переводить нечего).
- Новые переводы: cron-диалог ботов «Send results to» → «Отправлять результаты
  в», «Run history only» → «Только в историю запусков», опция
  «<имя>’s chat (bot responds)» → «<имя> — чат (отвечает бот)»; ошибки
  «Could not create the agent.» и «Could not create the profile yet»;
  «Toggle tabs» (правый клик) → «Переключить вкладки» + i18n-ключ
  `view.toggleTabStrip` в ru.ts.
- install.bat: транслит заменён на русский (chcp 65001).
- `EXPECTED_COMMIT` → `14c59f0b505` (актуальный апстрим).

## [1.0.1] - 2026-08-22

### Added

- Шаблоны GitHub Issues: «Баг / непереведённое» и «Doctor FAIL после апдейта».
- `bugs.url` в package.json → Issues (кнопка на npm).

### Changed

- README: официальная нумерация Hermes **0.20.5** (вместо календарных тегов),
  сжатая установка, блок «Обратная связь», пометка про регулярные обновления мода.
  Убран «Состав репозитория».

## [1.0.0] - 2026-08-22

### Added

- Публикация на npm: `npm install -g hermes-desktop-ru` + CLI `hermes-desktop-ru install | doctor | help`.
- Репозиторий стал публичным.

### Changed

- Новая нумерация: 1.0.0 — стабильный публичный релиз; линия 7.6.x объявлена legacy.
- `EXPECTED_COMMIT` обновлён под апстрим `1bf8bd2c7d2` (0.20.5, doctor 637/637).

### Fixed

- Окно «Hermes couldn't start» (BootFailureOverlay) больше не откатывается на
  английский при недоступном бэкенде: выбранная локаль сохраняется в localStorage
  и используется как fallback, когда `/api/config` не отвечает (раньше
  `context.tsx` сбрасывал язык в дефолтный `en` в `.catch`).
- Переведены хардкод-сообщения main-процесса об ошибках удалённого шлюза:
  «Could not reach the remote Hermes gateway while refreshing its WebSocket
  ticket…» и «Your remote gateway session has expired…» (`electron/main.ts`),
  а также сообщения теста соединения «Reached the gateway over HTTP…»
  (`electron/connection-config.ts`) — видны в окне ошибки запуска и в
  настройках Шлюза.
