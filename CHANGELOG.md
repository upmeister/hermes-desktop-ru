# Changelog

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).
Версии мода не совпадают 1:1 с версиями Hermes Desktop.

> Нумерация начата с 1.0.0 — это первый стабильный публичный релиз.
> Предыдущая линия 7.6.x (август 2026) считается тестовой и здесь не описывается;
> её историю можно посмотреть в git-истории репозитория.

## [1.2.2] - 2026-08-28

### Added
- Переводы нового апстрима 0.20.6: Managed updates (SSH-инсталляции под управлением
  Desktop), keychain-шифрование секретов, fleet-рейл профилей шлюзов, read-only
  транскрипты, hydration-оверлей, предупреждение смены модели (cron), Pop in/Pop out,
  Open in external, раздел «Браузер» (useRealProfile + описание), заголовок Sidebar.
- Вкладка «Боты»: Активность группы (заголовок, Show/Hide), кнопка «Стоп» (обе
  позиции), тултип Stop, статусы capped/held/stopped, плейсхолдер нового бота.
- Реестр: 946 → **953 правила** (doctor 953/953, GATE 0).
- tsc-гейт сборки zip: `files/*.ts` проверяются на синтаксис перед упаковкой
  (прецедент: пропущенная запятая ломала сборку у пользователя).

### Fixed
- `--allow-stale-dist`: честная диагностика, когда `package/dist` отсутствует
  в поставке (раньше флаг молча падал в ту же сборку).
- Session unavailable / Cloud session expired: правила переписаны на новые формы
  якорей (апстрим изменил строки) — ошибки снова переведены.
- Удалены мёртвые правила: дубликаты волн 3–5 с устаревшими отступами,
  тестовое правило expansion, wake-word hint (строка исчезла из апстрима).

## [1.2.1] - 2026-08-26

### Added
- Волна переводов «слепых зон»: Боты (статусы провайдеров, continuous chat, Hourly),
  композер (Attach a file/folder/…), биллинг (Auto-refill, Remote Spending), канбан
  (help-подсказки колонок), MCP-каталог (Jira/Linear/Figma/Sentry/Datadog), ошибки
  сессий (Session unavailable / Couldn't open this session), split-меню «Вверх».
- Реестр: 865 → **946 правил** (doctor 946/946, GATE 0).
- `.gitattributes`: LF для `sh`/`mjs`, CRLF для `bat`/`ps1`.
- Asar: `win-arm64-unpacked` / `linux-arm64-unpacked`; walk ищет `resources`
  без учёта регистра (только под `apps/desktop/release/`).
- `check.yml`: матрица ubuntu + windows. На Linux — `bash install.sh --self-test`
  и проверка +x. На Windows `--self-test` спавнит `npm.cmd --version` с `shell: true`.
- `--self-test`: на фейковом дереве выбирает нативный layout (win/linux/mac + arch).
- Issue-шаблоны: поля «ОС» и «как собран Desktop».

### Fixed
- README.en: совместимость 0.20.5 — doctor 865 (1.2.0), не 859/1.1.1.

## [1.2.0] - 2026-08-25

### Added
- Кроссплатформенный установщик на Node (`package/install.mjs`) — источник истины.
  PowerShell / BAT остаются обёрткой для двойного клика на Windows; `install.sh` — для POSIX.
- Резолв клона: `--root` → `HERMES_AGENT_ROOT` → `HERMES_INSTALL_DIR` →
  `$HERMES_HOME/hermes-agent` → `~/.hermes/hermes-agent` →
  `/usr/local/lib/hermes-agent` → `%LOCALAPPDATA%\hermes\hermes-agent`.
- Резолв asar только внутри клона: `win-unpacked` / `linux-unpacked` /
  `mac[-arm64|-x64]/Hermes.app/Contents/Resources`. Официальный `.app` / AppImage
  с сайта не трогаем.
- `node package/install.mjs --self-test` — проверка резолва без клона Hermes.
- CI: `check.yml` гоняет self-test. `experimental-posix.yml` (`workflow_dispatch`) —
  self-test на ubuntu+macos и опциональный doctor против shallow-клона апстрима
  (без `npm run pack`, без UI).
- README: Linux/macOS помечены как экспериментальные; автор на них установку не гонял.
- Переводы: `vibeHeartsTitle`/`vibeHeartsDesc` (тумблер Vibe Hearts),
  `view.selectionToComposer` (ренейм), `newTab`; окно создания бота/агента в
  `hermes-bots` (Provider/Model (Custom), Capabilities, SOUL.md, remote-заметка).
- Реестр doctor: 859 → **865 правил**. Удалён мёртвый перевод
  `auxiliary.tasks.web_extract` (label/hint — ключ убран апстримом).
- `AUTHORS.md`: атрибуционный текст от первого лица.

### Changed
- CLI больше не вызывает `powershell.exe`. `package.json`: снят `"os": ["win32"]`.
- Kill процессов — по пути клона/pack, не по имени `hermes` (CLI не гасим).
- На darwin после подмены asar — best-effort ad-hoc `codesign --sign -`.
- README.ru / README.en переписаны (структура та же; конвенции перевода сжаты).

## [1.1.1] - 2026-08-25

### Added
- Электрон-меню приложения (main-process): «Проверить обновления…», «О программе»,
  «Новое окно», «Открыть папку…», масштаб (Увеличить/Уменьшить/Фактический
  размер), «Справка», «Инструменты разработчика» — 12 правил на electron-меню.
- Диалоги сохранения (Сохранить файл ×3, Сохранить изображение) и «Обновление
  Hermes» — main-process хардкоды.
- Облачные уведомления: «Войти в Hermes Cloud», «Обновляем сессию…», OAuth-окно.
- Disband-диалог (апстрим переписал удаление группы Delete → Disband):
  оба диалога переведены (title «Расформировать групповой чат?», описание,
  кнопки, notify) — 7 правил.
- README: возвращены конвенции перевода + бэкенд-очерк (что не переводим,
  что патчим).

### Changed
- Реестр: 703 → **859 правил**.
- README: шапка v1.1.1, doctor 859/859 в таблицах обоих README.
- UPSTREAM-WATCH: восстановлена шапка журнала (авто-запись её затёрла).

### Fixed
- Wake-word подсказка бэкенда (tui_gateway/server.py): правило применено,
  но вывод бэкенда виден только после полного перезапуска Desktop (живой
  процесс держит старый код). Записано как класс проблем в бэклог.

## [1.1.0] - 2026-08-24

### Added
- Групповые чаты Bots: перевод всего группового фида активности (10 глаголов
  `is working…`/`replied`/`took too long`/`hit an error`/`turn settled`/…),
  `Group settings`, «N из M доступно», фильтр ростера (`Filter roster`,
  «Активные давно»), подпись панели «Чат бота» (tabTitle, имя сессии в БД
  не трогается), тултипы устройств («локально/удалённо»), `You` → «Вы».
- Интер-агентные заголовки ядра: `Message from …`, `Replied to …`,
  `show message`/`show reply`, `Messaging/Messaged` (agent-delivery,
  user-message, assistant-message).
- i18n: `zones.showTabStrip`/`hideTabStrip`, `gatewayConnectionLostDetail`,
  `auxiliary.tasks.review`, `statusbar.gatewayUnavailable`.

### Changed
- Registry: 647 → **703 правила** (пересъёмы и delete через overrides).
- Удалён `docs/screenshot.png` (обзорный скрин — больше не используется в README).
- `*.zip` в `.gitignore` (временные файлы тестовых сборок).

### Fixed
- `Group settings — rename …` тултип: апстрим сменил `title:` → `label:`,
  старый якорь молча умер — переснят на новую форму.
- Doctor больше не валит установку из‑за косметического `AMBIGUOUS` (живой кейс
  24.08: `children: 'Retry'` и `title: 'Bots'` по два раза в переписанном
  `hermes-bots/plugin.js` при `CRITICAL_MISSING=0`). FAIL только если пропал
  *файл* критичного правила (kanban / connection-registry).
- `apply-hardcodes.mjs` не abort'ит процесс на косметических MISSING/AMBIGUOUS
  (раньше `exit 1` после частичной записи). Косметика skip, установка идёт.
- Сообщение «критичные правила / апстрим изменил логику» больше не врёт на
  любом неоднозначном литерале.

### Changed
- `hermes-bots/plugin.js` — зона cosmetic: из неё нельзя FAIL.
- `boot-failure-i18n-*` помечены `critical` (через overrides + fallback в движке).
- Порог `CRITICAL_MISSING ≥ 3` убран: 1–2 critical MISSING = WARN («фича мода
  выключена»), установка продолжается.
- `gen-registry.mjs` штампует `severity`, если его ещё нет: `insert-after` →
  `critical`, иначе `cosmetic`. Явный override побеждает.
- `apply-hardcodes.mjs` мержит `overrides.json` в рантайме — не обязательно
  перегонять registry, чтобы классификация доехала.

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
