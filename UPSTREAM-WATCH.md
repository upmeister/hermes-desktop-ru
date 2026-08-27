# UPSTREAM-WATCH — журнал наблюдения за апстримом Hermes

Автоматический журнал, который ведёт ИИ-агент (проверка ~каждые 2 часа,
вне пиковых часов API). Следит за репозиторием
[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent):

- новые релизы Hermes Desktop;
- коммиты по `apps/desktop`;
- изменения `en.ts` (новые ключи i18n).

Формат записей: время, затронутая версия/коммиты, новые ключи, что проверить
перед следующим релизом мода.

> Записи добавляются агентом автоматически. Коммит и пуш этого файла — вручную,
> при релизной работе.

## 2026-08-25 (release note, вручную)

- Релиз **v1.1.1**: merged-правила 703 → **859** (волна 5.5: electron-меню,
  диалоги сохранения, облачные уведомления, Disband-диалог). EXPECTED_COMMIT
  → `41447a6d706`. Doctor 859/859, 0 MISSING на ПК (w11). README: возвращены
  конвенции перевода + бэкенд-очерк.

## 2026-08-24 13:04 (auto)
- Релизы: нет
- Коммиты apps/desktop: 6 новых, первые 5 тем сообщений кратко: fix(desktop): polish HUD movement and resizing on X11; fix(desktop): add a HUD layout reset control; fix(desktop): keep the Linux HUD clickable and recoverable; fix(desktop): debounce and re-verify zoom on Linux Wayland; fix(desktop): move the Linux HUD with a native compositor drag
- Новые ключи en.ts: не удалось получить файл en.ts
- Что проверить перед следующим релизом мода: проверить en.ts файл вручную

## 2026-08-24 17:03 (auto)
- Релизы: v2026.8.19 (2026-08-21), v2026.8.18 (2026-08-18), v2026.8.16.2 (2026-08-17), v2026.8.16 (2026-08-16), v2026.8.13 (2026-08-13)
- Коммиты apps/desktop: 15 новых с прошлого прогона, первые 5 тем сообщений кратко: fix(desktop): float and pin the HUD on Hyprland,fix(desktop): never kill a healthy backend on a claim probe failure; surface real stderr (#93608),fix(desktop): polish HUD movement and resizing on X11,fix(desktop): add a HUD layout reset control,fix(desktop): keep the Linux HUD clickable and recoverable
- Новые ключи en.ts: нет изменений
- Что проверить перед следующим релизом мода: ничего срочного

## 2026-08-25 02:02 (auto)
- Релизы: нет
- Коммиты apps/desktop: 15 новых с прошлого прогона, первые 5 тем сообщений кратко: fmt(js): `npm run fix` on merge (#94046),fix(desktop): float and pin the HUD on Hyprland,fix(desktop): never kill a healthy backend on a claim probe failure; surface real stderr (#93608),fix(desktop): polish HUD movement and resizing on X11,fix(desktop): add a HUD layout reset control
- Новые ключи en.ts: нет изменений
- Что проверить перед следующим релизом мода: ничего срочного

## 2026-08-25 04:07 (auto)
- Релизы: нет
- Коммиты apps/desktop: 15 новых с прошлого прогона, первые 5 тем сообщений кратко: style(desktop): space sibling restore import for eslint; fix(desktop): restore pending_clarify snapshots on activate and resume; fix(desktop): re-arm pending clarify cards in place; fix(desktop): demote unanswered clarify cards on Stop; fix(desktop): stop transcript jumps when a turn settles
- Новые ключи en.ts: view.terminalSelection → view.selectionToComposer (ренейм, 'Send terminal selection to composer' → 'Send selection to composer'); newTab: 'New tab' — оба НЕ покрыты модом v1.1.0
- Что проверить перед следующим релизом мода: 1) view.selectionToComposer — новый ключ контекстного меню (отправка выделенного в composer), перевести; 2) newTab ('New tab') — новый ключ вкладок, найти контекст и перевести

## 2026-08-25 06:02 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 2 новых с прошлого прогона: fmt(js): `npm run fix` on merge (#94230) — только форматирование (clarify-tool.tsx, тесты); feat(tui-gateway): seq-stamped event replay for lossless desktop reconnect — реконнект-механика (tui_gateway/event_replay.py, use-gateway-boot.ts), UI-строк вне en.ts не добавляет
- Новые ключи en.ts: нет изменений (SHA 51b0e89232b98ca7 — совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: 1) LITERALS_UNCOVERED упал 27→7: 20 литералов (бот-гейтвей: Gateway removed/On demand/Bot Mode, группы: Disband/New thread in/Delete Group, cronjob-детали, New Bot…) ушли из «непокрытых» НЕ из-за апстрима, а из-за WIP в рабочем дереве (overrides.json +1173 строки, i18n/ru.ts ±61, EXPECTED_COMMIT → a0ca7c19204) — при релизе WIP сверить осознанность правил; 2) feat 87631bd8aeb1 — новая механика реконнекта tui-gateway (seq-replay), при следующем релизе мода убедиться, что EXPECTED_COMMIT/targets не разъехались с HEAD апстрима

## 2026-08-25 10:08 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 9 новых с прошлого прогона, первые 5 тем сообщений кратко: test(desktop): cover UI scale across recordless hash routes; fix(desktop): keep UI scale across in-page route navigation; fix(desktop): stop gating edit-menu Paste on the clipboard probe (#91553); fix(desktop): keep modal context menus inside dialogs; fmt(js): `npm run fix` on merge (#94346)
- Затронутые файлы → куда смотреть в UI: i18n/en.ts (93acc22a9f29) → Настройки, секция Floating Composer / Message Reactions — новый тумблер Vibe Hearts; роутинг-навигация (b637ee0fc683, recordless hash routes) → переключение сессий/вкладок — масштаб UI не должен сбиваться; electron-меню (5400fb88e5bd, e3b5512b7b3f) → Edit→Paste и контекстные меню внутри модальных диалогов
- Новые ключи en.ts: vibeHeartsTitle ('Vibe Hearts'), vibeHeartsDesc (парящие сердечки за thanks/ily/good bot/heart) — оба НЕ покрыты модом v1.1.0 (в registry.json и ru.ts, включая WIP, отсутствуют)
- Что проверить перед следующим релизом мода: 1) перевести vibeHeartsTitle/vibeHeartsDesc (Настройки → тумблер Vibe Hearts, рядом с Floating Composer/Message Reactions); 2) вижн-тест: новый тумблер Vibe Hearts и стабильность масштаба UI при навигации между сессиями

## 2026-08-25 12:19 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 2 новых с прошлого прогона: test(desktop): stop the syntax-diff mock factory from leaking unhandled rejections (#94415); feat: browser snapshots drop LLM summarization — truncate-and-store like web_extract; auxiliary.web_extract slot removed
- Затронутые файлы → куда смотреть в UI: i18n/en.ts (a75ea37dc5a8) → пикер вспомогательных моделей/задач — пункт «Web extract» (auxiliary.tasks.web_extract) удалён из списка aux-задач; c1b295d003f6 — только тест, без UI-поверхности
- Новые ключи en.ts: нет новых ключей — удалён auxiliary.tasks.web_extract ('Web extract'/'Page summarization'); модом v1.1.1 уже покрыт (ru.ts:993 «Веб-извлечение») → перевод стал для мода мёртвым
- Что проверить перед следующим релизом мода: 1) auxiliary.tasks.web_extract удалён апстримом — при следующем релизе убрать мёртвый перевод «Веб-извлечение» из ru.ts (или оставить осознанно, безвредно); 2) вижн-тест: в списке вспомогательных задач (пикер моделей) больше нет пункта Web extract/«Веб-извлечение»

## 2026-08-25 14:11 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 0 новых с прошлого прогона (список 15 коммитов неизменён)
- Затронутые файлы → куда смотреть в UI: изменений апстрима нет
- Новые ключи en.ts: нет изменений (EN_TS_SHA 308fc8fbd9ab90c4 совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: ничего срочного (LITERALS_UNCOVERED=7 из plugin.js — локальный WIP overrides.json, не апстрим)
## 2026-08-25 (release note, вручную)

- Релиз **v1.2.0**: кроссплатформенный Node-установщик (`package/install.mjs` —
  источник истины; PS/BAT/sh — тонкие обёртки; POSIX экспериментально,
  официальные .app/AppImage не трогает). CI: `check.yml` + `experimental-posix.yml`
  (workflow_dispatch, ubuntu+macos). merged: 859 → **865** правил (+6 — окно
  создания бота: Provider/Model (Custom), Capabilities, SOUL.md, remote-заметка).
  i18n: vibeHearts, selectionToComposer (ренейм), newTab, +12 по L3 (pets,
  тулсеты, ssh-хост, блокеры обновления); удалён мёртвый `web_extract`.
  EXPECTED_COMMIT → `6ce7ab8bfb` (HEAD ПК). README RU/EN переписаны
  (установщик/CI/POSIX), шапки v1.2.0 · doctor 865. AUTHORS.md — от первого лица.

## 2026-08-25 22:05 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 0 новых с прошлого прогона (список 15 неизменён; свежие коммиты репо — web/mcp/docs, не desktop)
- Затронутые файлы → куда смотреть в UI: апстрим не менялся — en.ts (308fc8fbd9ab90c4) и plugins/hermes-bots/plugin.js без новых коммитов; изменение вывода датчика — ЛОКАЛЬНЫЙ WIP, не апстрим: package/overrides.json обновлён 21:26 (после прогона 14:11), +329/−58, массовые delete-правила hermes-bots-* → покрытие литералов сдвинулось
- Новые ключи en.ts: нет изменений (SHA совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: 1) LITERALS_UNCOVERED 7→9: причина — незакоммиченный WIP overrides.json (21:26), при релизе сверить осознанность delete-правил; 2) 9 непокрытых литералов plugin.js (вкладка «Боты»): 6 технических (комментарий 'Bot Chat', значение опции 'deny', плейсхолдеры Provider/Model — omnirouter/9router/nous, antigravity/gemini-3.6-flash-high, cron-пример 'every 1d · every 2h · 0 9 * * * (cron)') — не переводить; 3 переводимых шаблона: 'Some sections failed: …' (настройка секций), 'Could not send the answer to @…' (ошибка отправки в групповой чат), 'e.g. omnirouter, inferx, 9router' / 'e.g. antigravity/…' (примеры — «напр.») — решить, закрывать ли

## 2026-08-26 00:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 0 новых с прошлого прогона (список 15 неизменён; RELEASES/COMMITS/EN_TS_SHA совпадают с прогоном 22:05)
- Затронутые файлы → куда смотреть в UI: апстрим не менялся; изменение вывода датчика — ЛОКАЛЬНОЕ: сканер literals.py расширен 23:54 (паттерн «любой ключ: 'Строка'», +94 реальных на чистом апстриме), overrides.json WIP обновлён 23:18 (+869/−58) → в неизменённом plugins/hermes-bots/plugin.js теперь видно 18 непокрытых литералов (было 9) → вкладка «Боты» (менеджер скиллов, профиль/черновик бота, cronjob-настройки, статус шлюза, групповой композер)
- Новые ключи en.ts: нет изменений (EN_TS_SHA 308fc8fbd9ab90c4 совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: 1) 11 вновь обнаруженных непокрытых литералов plugin.js — НЕ апстрим-дрейф (строки уже были в файле, сканер стал зорче): «Hit "+ Add to this Agent"…» (9273, скиллы), «Name the bot first…» (10262, черновик бота), cronjob-ошибки/опции (10601/10615/10619/10966/10978), «Checking image backend…» (4337), «Keep this exact face…» (4218), «Waiting for the gateway connection…» (14622), «New group conversations…» (15171) — решить, переводить ли; 2) ⚠️ регрессия сканера: 2 backtick-шаблона («Some sections failed…» plugin.js:9534, «Could not send the answer to @…» :12311) больше не извлекаются новым паттерном — строки на месте, но выпали из наблюдения (поправить literals.py, если возвращать); 3) WIP overrides.json +869/−58 — при релизе сверить осознанность правил

## 2026-08-26 (release note, вручную)

- Релиз **v1.2.1**: POSIX-followup overlay (ARM unpacked-пути, walk resources
  без регистра, self-test с нативным layout + npm.cmd spawn на Windows,
  check.yml матрица ubuntu+windows, .gitattributes EOL, issue-шаблоны WSL)
  **+ волна 5.6** (59 правил слепых зон: боты/композер/биллинг/канбан/MCP/
  preview/session). merged: 865 → **946**. EXPECTED_COMMIT → `6ce7ab8bfb`.
  Doctor 946/946, GATE 0.
## 2026-08-26 02:05 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 2 новых с прошлого прогона: 02c7ae956e42 fix(desktop): route session list REST through the active profile; 90ee4460cb45 fix(desktop): translate sidebar recents_profile through SSH aliases
- Затронутые файлы → куда смотреть в UI: src/api/sessions.ts (список сессий в сайдбаре — недавние/крон/чат теперь грузится через scope активного профиля: при remote/мультипрофильном подключении вкладка «Недавние» могла показывать не тот профиль); electron/connection-config.ts (подключение к серверу через SSH-алиас: профиль «Недавних» в сайдбаре теперь корректно транслируется на remote-профиль вместо remote-default)
- Новые ключи en.ts: нет изменений (EN_TS_SHA 308fc8fbd9ab90c4 совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: ничего срочного — оба коммита логика роутинга запросов, i18n/строки не затронуты; LITERALS_UNCOVERED=18 — тот же локальный WIP overrides.json (не апстрим)

## 2026-08-26 06:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 4 новых с прошлого прогона (02:05): feat(desktop): open a Browser tab in the default browser from its context menu; feat(desktop): let a pane prefix the zone tab menu; style(desktop): sort secret-storage-policy import per perfectionist lint; feat(desktop): OS-keychain encryption for stored secrets is now opt-in — no more macOS Keychain password prompt on every launch
- Затронутые файлы → куда смотреть в UI: app/settings/gateway-settings.tsx + electron/secret-storage-policy.ts (6a6e16fa5d) → Настройки → вкладка шлюза/подключений, секция сохранения секретов (рядом с «Test remote» и «Save for next restart») — новый тумблер шифрования секретов системной связкой (Keychain/GNOME Keyring/DPAPI); app/chat/preview-tile.tsx (26777a4178) → контекстное меню вкладки Browser (превью) — новый пункт «Open in external»; components/pane-shell/* (b9513f2e1d) → меню вкладок зон — префикс имени панели (i18n не затронут)
- Новые ключи en.ts: keychainEncryptionTitle ('Encrypt saved secrets with the OS keychain'), keychainEncryptionDesc (описание шифрования Keychain/GNOME Keyring/DPAPI), keychainEncryptionFailed ('Could not change secret encryption') — из 6a6e16fa5d; openInExternal ('Open in external') — из 26777a4178. Все 4 НЕ покрыты модом v1.2.1 (0 совпадений в i18n/ru.ts, package/registry.json, overrides.json)
- Что проверить перед следующим релизом мода: 1) перевести keychainEncryptionTitle/Desc/Failed (Настройки → шлюз, тумблер «шифровать секреты системной связкой») и openInExternal (контекстное меню вкладки Browser); 2) вижн-тест: тумблер шифрования секретов (по умолчанию выкл — opt-in) и пункт меню «Open in external»; 3) LITERALS_UNCOVERED=18 — без изменений, локальный WIP overrides.json (не апстрим)
## 2026-08-26 12:06 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 15 новых с прошлого прогона (после записи 06:01 список целиком сменился), первые 5 тем сообщений кратко: test(desktop): pin the clock in the session-row timestamp test; fix(desktop): stop the Bots roster hanging on a live profile; fix(desktop): skip Tip delay when moving between adjacent chrome; fix(desktop): keep the Cronjobs pane subscribed to roster hydration; fmt(js): `npm run fix` on merge (#95114)
- Затронутые файлы → куда смотреть в UI: plugins/hermes-bots/plugin.js (458f26c0dc9e, b73e057855a4, 250faa69fb79, 936a6ea8f7ce) → вкладка «Боты» — зависание ростера на живом профиле, краш диалога New Cronjob (owner — roster-объект), панель Cronjobs (подписка на ростер, скоуп на выбранного бота); Browser pop-out (a608799689e4, e8df4017386e, 30b042e137a5) → контекстное меню вкладки Browser: «Pop out» — собственное окно ОС, вкладка скрывается в доке, «Pop in» — вернуть; очистка JS/TS-ошибок при pop-out; editor-композер (37a8c10ab125) — таймеры редактирования не живут дольше композера (i18n не затронут)
- Новые ключи en.ts: popIn ('Pop in'), popOut ('Pop out') — из a608799689e4/e8df4017386e (контекстное меню вкладки Browser: вынести в окно ОС / вернуть в док). НЕ покрыты модом v1.2.1: 0 совпадений в registry.json, i18n/ru.ts, package/files/ru.ts, overrides.json (composerPopoutTitle/Desc — другой ключ, уже переведён)
- Что проверить перед следующим релизом мода: 1) перевести popIn/popOut (ПКМ по вкладке Browser → Pop out / Pop in); 2) вижн-тест: pop-out в отдельное окно ОС, скрытие вкладки в доке, pop-in обратно; 3) LITERALS_UNCOVERED=18 — набор тот же, что в записи 00:01, но plugin.js апстримно обновился (все позиции сдвинуты +4 строки) — решения по строкам уже приняты, нового нет

## 2026-08-26 14:12 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 15 новых с прошлого прогона (после 12:06 список целиком сменился), первые 5 тем сообщений кратко: fmt(js): `npm run fix` on merge (#95329); fix(desktop): first Windows update attempt no longer fails on dying backend processes (#74805); fix(desktop): pin the complete macOS usage-description set + add reminders entitlement; fix(desktop): declare NSAppleMusicUsageDescription to disclaim MediaLibrary TCC prompt; fix(desktop): declare NSLocalNetworkUsageDescription for macOS 15+ (#81563)
- Затронутые файлы → куда смотреть в UI: electron/backend-release-gate.ts + electron/main.ts (b04f8578eb68) → флоу обновления, системные диалоги (первый апдейт на Windows больше не падает на умирающих процессах бэкенда); app/session/hooks/use-session-actions (718654a9a234, add24666d53c, cab6c4f70bdc) → действия сессий messenger (delete/archive) — маршрутизация на владеющий профиль, тосты/алерты ошибок; electron/main.ts (a70e7b0ca739, d77114d0d0e6, 7944ad2168a8) → SSH-маршрутизация терминалов (по окнам, через registry) — поведение, строк не добавляет; macOS entitlements/TCC-декларации (a7eee2a7a775, f0e990266446, 5d286654103b, fc323cedf5dc, 8d27e1dfd07e) → системные TCC-промпты macOS, официальный .app (установщик мода их не трогает)
- Новые ключи en.ts: нет изменений (EN_TS_SHA 55a058430cab9381 совпадает с прогоном 12:06)
- Что проверить перед следующим релизом мода: 1) вижн-тест: первый апдейт на Windows (диалог обновления) не падает при живом бэкенде — поведенческий фикс, i18n не затронут; 2) delete/archive сессий messenger и SSH-маршрутизация терминалов — логика, новых строк нет (en.ts и литералы не изменились); 3) LITERALS_UNCOVERED=18 — набор и позиции совпадают с прогоном 12:06, решения приняты, нового нет

## 2026-08-26 16:09 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: окно 15 целиком сменилось с прошлого прогона (по since-фильтру с 14:12 +07 — 37 новых коммитов; датчик зафиксировал изменение в пиковое окно 06–10 UTC, поэтому печатал UNCHANGED, а не CHANGED — pending=381a6d63c81380bc), первые 5 тем сообщений кратко: fix(desktop): clicking a bot no longer burns a model turn on a fake user prompt; fmt(js): `npm run fix` on merge (#95365); fix(desktop): drop unused registryGatewayWsUrl import left by the header-binding refactor rebase; fix(desktop): recover remote sessions after gateway restart; fix(desktop): log when Windows remote SSH skip teardown
- Затронутые файлы → куда смотреть в UI: plugins/hermes-bots/plugin.js (4faa721d7d2b) → вкладка «Боты»: клик по боту в ростере больше не сжигает turn модели на фейковом user prompt — чат открывается без лишнего вызова модели; app/settings/gateway-settings.tsx + components/boot-failure-overlay.tsx + electron/native-oauth.ts (21f34794beb1, 949f5169dee7) → Настройки → шлюз и оверлей ошибок загрузки: remote-сессии восстанавливаются после рестарта шлюза, ticket 401 при нечитаемых нативных токенах → sign-in; electron/main.ts (0c69cac48a88, 8085614f6a27, b4162de3339b, 25d46c788746) → SSH-бэкенды/WS-заголовки — поведение, строк не добавляет
- Новые ключи en.ts: нет изменений (EN_TS_SHA 55a058430cab9381 совпадает с прогоном 14:12)
- Что проверить перед следующим релизом мода: 1) вижн-тест: вкладка «Боты» — клик по боту открывает чат без фейкового промпта (поведенческий фикс, i18n не затронут); 2) Настройки → шлюз / оверлей загрузки: recovery remote-сессий после рестарта шлюза, 401→sign-in (нативные токены) — логика, новых строк нет; 3) LITERALS_UNCOVERED=18 — набор тот же, позиции сдвинулись (plugin.js апстримно обновился), решения приняты, нового нет
## 2026-08-26 18:02 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 16 новых с прошлого прогона (окно целиком сменилось), первые 5 тем сообщений кратко: fmt(js): `npm run fix` on merge (#95457); style(desktop): sort registrySourceOwnsPrimaryBackend imports (lint); refactor(desktop): one canonical write shape for connection_id row stamping; fix(desktop): stamp remote list rows with their owning connection; retry one transient projects.tree loss; fix(desktop): bound the boot descriptor wait so a dead primary cannot strand the registry restore
- Затронутые файлы → куда смотреть в UI: src/api/sessions.ts + src/store/projects.ts (2947272233fb, fb393ee08b73) → сайдбар «Недавние»/список сессий — remote-строки помечаются своим подключением, retry при потере projects.tree; store/connections.ts + electron/connection-registry.ts + electron/main.ts (b2a58dbb39cf, fd031488aa0f) → загрузка/восстановление подключений — ждём primary descriptor, мёртвый primary не подвешивает restore; app/contrib/wiring* + app/session/hooks/* + store/gateway.ts (d6e323bd63fb, c662e1be7b5e, 6fdf873464ea, 962b308be184, 07b87f1470ae, cb75983abfdc, 77edf1b4df12) → новые чаты из профиль-рейла, переключение профилей, статус шлюза — точный владелец сессии от создания до RPC (i18n не затронут)
- Новые ключи en.ts: нет изменений (EN_TS_SHA 55a058430cab9381 совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: 1) вижн-тест: remote-строки в «Недавних» и восстановление подключений при загрузке — dead primary больше не блокирует restore (поведение, строк нет); 2) новые чаты из профиль-рейла и переключение профилей — сессия сохраняет владельца от создания до всех последующих RPC; 3) LITERALS_UNCOVERED=18 — набор тот же, позиции сдвинулись (plugin.js апстримно обновился), решения приняты, нового нет

## 2026-08-26 20:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 13 новых с прошлого прогона (после 18:02; окно 15, 2 общих — c427367938ea/8e9459c97f70), первые 5 тем сообщений кратко: fmt(js): `npm run fix` on merge (#95511); fix(desktop): skip macOS TCC-protected media dirs in git repo scan; fix(desktop): single-owner backend dial claim in Electron main (#90812); fix(desktop): revalidate pooled remote/SSH backends on power resume (#93910); fix(desktop): poll-guard reset is fire-and-forget off the redial path
- Затронутые файлы → куда смотреть в UI: electron/git-repo-scan.ts + electron/backend-dial-claim.ts + electron/connection-registry.ts + electron/main.ts + electron/remote-liveness.ts (1bd5da3ac6, bb3421bf25, 3123624c07, fe615a0099) → подключения к серверам: один владелец dial'а за раз, remote/SSH-бэкенды ревалидируются при выходе из сна, на macOS TCC-папки (Фото/Музыка) пропускаются в скане git-репо — всё поведение, строк нет; app/chat/sidebar/connection-switcher.tsx + use-gateway-boot.ts (fe615a0099) → сайдбар → свитчер подключений: registry перепубликуется рендерерам после каждого успешного сохранения; app/chat/composer/status-stack/index.tsx + store/composer-status.ts + session-state-cache.ts + plugins/hermes-bots/plugin.js (c19849cd02, 06be6cffbc, d22e2b9f6e) → композер: статус-стек не штормит мёртвую сессию 4001s, reconnect-транскрипты освобождаются, canonical-title race — заголовок чата выбирает победителя вместо форка «forever chat»
- Новые ключи en.ts: нет изменений (EN_TS_SHA 55a058430cab9381 совпадает с прогоном 18:02)
- Что проверить перед следующим релизом мода: 1) вижн-тест: свитчер подключений в сайдбаре обновляется сразу после сохранения настроек подключения (перепубликация registry рендерерам); 2) композер/чат ботов: статус-стек больше не долбит мёртвую сессию, заголовок не форкается при гонке; 3) LITERALS_UNCOVERED=18 — набор тот же, позиции сдвинулись (plugin.js +19 строк), решения приняты, нового нет

## 2026-08-27 00:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: окно 15 целиком сменилось с прошлого прогона (общих нет); вне окна зафиксированы 2 коммита, меняющих en.ts — dd0aae4173 и fd565c80e9. Первые 5 тем сообщений кратко: fix(desktop): guard setPrimaryGatewayConnectionId against non-primary active scopes; fix(desktop): preserve primary gateway identity across source switches; fix(desktop): route clarify responses through session owner; fix(desktop): resolve session owners from the cron and messaging sidebar slices; chore: eslint --fix on salvaged e2e spec
- Затронутые файлы → куда смотреть в UI: app/chat/sidebar/fleet-rail.ts + profile-switcher.tsx + connection-switcher.tsx + connection-glyph.tsx + app/profiles/delete-profile-dialog.tsx + rename-profile-dialog.tsx + store/fleet-roster.ts (fd565c80e9) → сайдбар: новая fleet-лента профилей — агенты ВСЕХ зарегистрированных шлюзов в одной ленте (profile-switcher), недоступный шлюз помечается «unreachable», диалоги удаления/переименования профиля показывают шлюз («… on {gateway}»); app/chat/chat-swap-overlay.tsx + sdk/index.ts + store/profile.ts (dd0aae4173) → чат ботов: сохранённая история Bot Chat отрисовывается сразу, оверлей подмены чата с «Syncing {profile}…» при гидрации
- Новые ключи en.ts: fleet.* (6 шт: allOnGateway 'All profiles on this gateway', gateway 'Profiles on {gateway}', gatewayUnreachable '{gateway} · unreachable', onGateway '{name} · {gateway}', switchTo 'Switch to {name} on {gateway}', deleteOn ' on {gateway}') — из fd565c80e9; hydrationSyncing 'Syncing {profile}…' — из dd0aae4173. EN_TS_SHA bbef891ef844e82f (был 55a058430cab9381). НЕ покрыты модом v1.2.1: 0 совпадений в i18n/ru.ts, package/files/ru.ts, package/registry.json, overrides.json
- Что проверить перед следующим релизом мода: 1) перевести fleet.* (сайдбар → лента профилей всех шлюзов: «Switch to {name} on {gateway}» в свитчере, «unreachable» для недоступного шлюза) и hydrationSyncing (оверлей гидрации чата бота «Syncing {profile}…»); 2) вижн-тест: fleet-рейл в сайдбаре (переключение на профиль другого шлюза, пометка недоступного), подмена чата бота с оверлеем синхронизации; 3) LITERALS_UNCOVERED=18 — набор тот же, позиции сдвинулись (plugin.js +25..78 строк), решения приняты, нового нет

## 2026-08-27 02:04 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 3 новых с прошлого прогона (f0187332d1, b519ce29ad, d0fdbfd65; из окна ушли 2fa39fac8c81, f72786f764db, 9aa7530f7b53), первые 5 тем сообщений кратко: fix(desktop): decode-probe app icon candidates instead of existence-only (#94806); fix(desktop): keep attachment close and code copy icons visible (#95611); fix(desktop): show repo-root-only sessions in project drill-in (#94552)
- Затронутые файлы → куда смотреть в UI: electron/app-icon.ts + electron/main.ts (f0187332d1) → иконки приложений: кандидаты проверяются decode-пробой, а не существованием — иконки в доке/переключателе задач и системных диалогах рендерятся корректно для бандлов без иконки; app/chat/composer/attachments.tsx + components/chat/shiki-highlighter.tsx (b519ce29ad) → композер: крестик закрытия вложения и иконка копирования кода остаются видимыми (не схлопываются); app/chat/sidebar/projects/workspace-groups.ts (d0fdbfd65514) → сайдбар → Проекты: сессии на корне репо показываются в drill-in
- Новые ключи en.ts: нет изменений (EN_TS_SHA bbef891ef844e82f совпадает с прогоном 00:01)
- Что проверить перед следующим релизом мода: 1) вижн-тест: иконки вложений (крестик) и копирования кода не исчезают, сессии корня репо видны в drill-in «Проекты» — всё поведение, i18n не затронут; 2) LITERALS_UNCOVERED=18 — набор и позиции совпадают с прогоном 00:01, решения приняты, нового нет; 3) en.ts не менялся — новых переводов не требуется

## 2026-08-27 04:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 2 новых с прошлого прогона (68518c1f9bca, 01e9b9abb1f1; из окна ушли 35ee27b1c644, 7c255dbbbfc3), темы сообщений: fix(desktop): hold the sessions list refresh for the whole typing burst; fix(desktop): defer heavy sessions.changed list refresh while typing
- Затронутые файлы → куда смотреть в UI: app/contrib/hooks/use-background-sync.ts (+test) → список сессий (сайдбар «Недавние»/ростер, строка поиска/фильтра): тяжёлый refresh по sessions.changed откладывается и удерживается на всю серию ввода — список не дёргается/не тормозит, пока печатаешь (поведение, строк не добавляет)
- Новые ключи en.ts: нет изменений (EN_TS_SHA bbef891ef844e82f совпадает с прогоном 02:04)
- Что проверить перед следующим релизом мода: 1) вижн-тест: при вводе в поле фильтра сессий список не обновляется/не мигает до конца серии ввода (быстрый набор текста → один refresh в конце) — поведенческий фикс, i18n не затронут; 2) LITERALS_UNCOVERED=18 — набор и позиции совпадают с прогоном 02:04, решения приняты, нового нет

## 2026-08-27 06:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03)
- Коммиты apps/desktop: 13 новых с прошлого прогона (окно 15, 2 общих — 68518c1f9bca, 01e9b9abb1f1), первые 5 тем сообщений кратко: fix(desktop): session rows are identified by (profile, id) — twins in two profiles stop collapsing and misattributing; fix(desktop): SSH orphan reaper fails CLOSED on remote lockfile schema/ownership skew; fix(desktop): escape reloadUrl in error page inline script (script-tag breakout); fix(desktop): replace white screen after update with visible error + auto-reload (#95575); fix(desktop): put attachment close and code copy back on hover-reveal
- Затронутые файлы → куда смотреть в UI: app/chat/sidebar/index.tsx + sessions-section.tsx + virtual-session-list.tsx + store/session.ts + app/contrib/wiring.tsx (db127f7502) → сайдбар «Недавние»: строки сессий идентифицируются по (profile, id) — сессии-двойники в разных профилях больше не схлопываются и не путаются; electron/main.ts + window-renderer-lifecycle.ts + renderer-load-error-page.ts (c9d7b22e05b, 4bc84d0499) → оверлей ошибок рендерера: после апдейта вместо белого экрана — видимая ошибка + авто-reload, reloadUrl эскейпится (script-tag breakout); app/settings/model-settings.tsx + store/cron-model-impact.ts + i18n/en.ts (8fe4816edd) → Настройки → Модели / cron: подтверждение смены модели на guarded-тир («Model Selection Warning», трейд-офф, отмена) — ЕДИНСТВЕННЫЙ коммит с новыми строками en.ts; a2c3b54939 + 2f87fa66ad → композер/код-блоки: крестик вложения и копирование кода снова на hover-reveal (регресс-фикс после b519ce29ad), gating по hover media query убран; be7eefec8d → мысль ассистента: скролл в обрезанном thinking preview восстановлен; 19f9d1badb + store/onboarding.ts → онбординг fail-closed при model guard
- Новые ключи en.ts: cron.modelImpact.confirmTitle 'Model Selection Warning', confirmDetail 'Confirm only if you accept this trade-off.', confirmAction 'Confirm', declined 'Model change cancelled — you declined the data-training tier warning.' — из 8fe4816edd; EN_TS_SHA 521d403b9e62c0fe (был bbef891ef844e82f). НЕ покрыты модом v1.2.1: 0 совпадений (контекст cron.modelImpact) в i18n/ru.ts, package/files/ru.ts, registry.json, overrides.json
- Что проверить перед следующим релизом мода: 1) перевести cron.modelImpact.confirmTitle/confirmDetail/confirmAction/declined (Настройки → Модели: диалог подтверждения смены модели на data-training tier — «Model Selection Warning»); 2) вижн-тест: оверлей ошибки рендерера после апдейта (не белый экран), hover-reveal крестика вложения/иконки копирования кода не схлопывается (регресс-зона 26.08 b519ce29ad); 3) LITERALS_UNCOVERED=18 — набор тот же, позиции сдвинулись (plugin.js апстримно обновился), решения приняты, нового нет
## 2026-08-27 12:01 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03: v2026.8.19 21.08, v2026.8.18 18.08, v2026.8.16.2 17.08, v2026.8.16 16.08, v2026.8.13 13.08)
- Коммиты apps/desktop: 15 новых с прошлого прогона (после 06:01 окно целиком сменилось; 08:01/10:01 были в пике → pending), первые 5 тем сообщений кратко: fmt(js): `npm run fix` on merge (#96076); test(desktop): method-aware gateway mock for the refresh-reconcile confirm interaction test; fix(desktop): include route scope in gateway dial errors; fix(desktop): preserve group turn reason codes; fix(desktop): Bots-mode picker routes guarded model switches through the shared confirm handler
- Затронутые файлы → куда смотреть в UI: app/settings/managed-updates-section.tsx (НОВЫЙ) + app/settings/gateway-settings.tsx + store/managed-updates.ts (bc4eea77739c) → Настройки → Шлюз: новая секция «Managed updates» — обновление Desktop-managed SSH-инсталляций (Update/Updating…/Updated/Refused/failed, рецепты); plugins/hermes-bots/plugin.js (911978da62 #95279, 61b6788dd4, 477053538c73, a8169f3e65c5, 21054b751ec8) → вкладка «Боты»: пикер модели Bot Mode всегда settle (без remount churn), guarded-свитчи модели через общий confirm, route scope в ошибках dial, канал turn reason codes групп, скрытие unreachable близнецов ростера; electron/main.ts (1e73281614a0, ac2ec568333d) → claim-guard всех ensureBackend()/ensureRegistryBackend(), локальный профиль при SSH-switch (поведение)
- Новые ключи en.ts: managedUpdates.* (15 шт: title 'Managed updates', intro, sshConnection 'Desktop-managed SSH install', update, updating, progress, updated, partial 'Updated — restore failed', refused, failed, alreadyRunning, receipt `Receipt ${id} · ${outcome}`, receiptVersions `${pre} → ${post}`, scopesRestored `Restored profiles: ${profiles}`, scopeNotRestored `Profile "…" not restored`) — из bc4eea77739c; EN_TS_SHA 64976a73cc86e9f0 (был 521d403b9e62c0fe). НЕ покрыты модом v1.2.1: 0 совпадений в registry.json, overrides.json, i18n/ru.ts
- Что проверить перед следующим релизом мода: 1) перевести managedUpdates.* (Настройки → Шлюз → секция Managed updates для SSH-инсталляций: кнопка Update, прогресс, статусы и рецепты); 2) LITERALS_UNCOVERED 18→19: НОВЫЙ литерал «Model switch failed» (plugin.js:9829, пикер модели Bot Mode) — не покрыт; остальные 18 — тот же набор, позиции сдвинулись (+1..+49 строк), решения приняты; 3) вижн-тест: секция Managed updates на SSH-подключении (кнопка, Updating…, Updated/Refused/failed), пикер модели Bot Mode (confirm-диалог, no remount churn)
## 2026-08-27 14:02 (auto)
- Релизы: нет (те же 5, записаны 12:01: v2026.8.19 21.08, v2026.8.18 18.08, v2026.8.16.2 17.08, v2026.8.16 16.08, v2026.8.13 13.08)
- Коммиты apps/desktop: 2 новых с прошлого прогона (9f05b06589db, df7d7f6e8d6a; из окна ушли 1e73281614a0, b1f133d4ea12), темы сообщений: Revert "Merge pull request #94245 from kshitijk4poor/feat/gw-event-replay"; Merge pull request #94245 from kshitijk4poor/feat/gw-event-replay — фича пришла и сразу откачена
- Затронутые файлы → куда смотреть в UI: электрон/main.ts + electron/backend-command.ts + backend-ready.ts → запуск/готовность backend-процессов (поведение, строк нет); tui_gateway/event_replay.py + entry_ws.py + server.py + ws.py + apps/shared/json-rpc-gateway.ts + hermes_cli/dashboard.py → шлюз-события и их реплей (Python-сторона) — НО фича ревертнута, в shipped-коде отсутствует, вижн-тестить нечего
- Новые ключи en.ts: нет изменений (EN_TS_SHA 64976a73cc86e9f0 совпадает с прогоном 12:01)
- Что проверить перед следующим релизом мода: ничего срочного — merge+revert дают net-zero; если gw-event-replay вернут повторно, обратить внимание на tui_gateway/event_replay (подсказки/события шлюза). LITERALS_UNCOVERED=19 — набор тот же, plugin.js без изменений
## 2026-08-27 18:01 (auto)
- Релизы: нет (те же 5, записаны 12:01: v2026.8.19 21.08, v2026.8.18 18.08, v2026.8.16.2 17.08, v2026.8.16 16.08, v2026.8.13 13.08)
- Коммиты apps/desktop: 14 новых с прошлого прогона (окно 15, общий — 9f05b06589db), первые 5 тем сообщений кратко: test(desktop/bots): drop unused prompt params in empty-sentinel harness (lint); fix(desktop,bots): render "(empty)" sentinel as a friendly message in group chat; test(desktop/bots): pin harvestStrandedGroupReply's rescued-delivery path; fix(desktop/bots): keep a substantive group reply after a synthetic (pass); test(desktop): lock the Stop button to room.running and the stop primitive
- Затронутые файлы → куда смотреть в UI: plugins/hermes-bots/plugin.js (24a5b6ecb7, 411f9c2f44, 1ae2c2b171, 1b575c65ab, c5e0def79, 8d412e67ba, 42e0b5f24f, f05fec3565) → вкладка «Боты» / групповые чаты: кнопка Stop для раунда (#94570, #91868/#94569 — тултип «Stop this run…» НОВЫЙ), "(empty)" sentinel пустого ответа рендерится дружеским сообщением, continuation rounds + mention tracking после @-хендоффа; api/sessions.ts + session-owner-stamp.ts + use-session-tile-delegate.ts (9faa685385 #94724) → сайдбар «Недавние»/загрузка сессий: read-only resume сохранённых транскриптов + backfill владельца; electron/remote-lifecycle.ts (beb212dcc5) → remote/SSH-бэкенды: два бага managed-SSH-spawn, ломавших каждый свежий remote-бэкенд (поведение); components/assistant-ui/tool/fallback-model/* (65974a3e7c #96093) → строки browser_exec в сообщениях ассистента: заголовок берётся из ведущего #-комментария
- Новые ключи en.ts: нет изменений (EN_TS_SHA 64976a73cc86e9f0 совпадает с 12:01/14:02)
- Что проверить перед следующим релизом мода: 1) перевести «Stop this run — interrupts the member on turn and holds the rest» (вкладка «Боты» → групповой чат → кнопка Stop раунда, тултип; plugin.js:13515/13553 — 2 позиции, в моде 0 совпадений); 2) вижн-тест: Stop-кнопка группового раунда (прерывает участника и держит остаток), пустой ответ группы показывается как "(empty)"-сообщение, а не пропадает; 3) LITERALS_UNCOVERED 19→21: новые только «Stop this run…» ×2, остальные 19 — прежний набор (позиции сдвинулись: «Model switch failed» 9829→10145, «New group conversations…» 15171→15947), решения приняты
## 2026-08-27 20:04 (auto)
- Релизы: v2026.8.27 (27.08) — Hermes Agent v0.20.6, patch: роллап ~525 PR с v0.20.5 (консентный real-profile browsing, отдельное окно desktop Browser, managed SSH remote-update, MCP-каталог 50+ серверов, TTL-кэш web_search, lean-tail compression, OS-keychain шифрование секретов и др. — всё уже отслежено прошлыми прогонами); прочие 4 — те же (v2026.8.19 21.08, v2026.8.18, v2026.8.16.2, v2026.8.16)
- Коммиты apps/desktop: 3 новых с прошлого прогона (окно 15, старые 3 вытеснены), все темы: test(desktop/bots): drop unused prompt params in empty-sentinel harness (lint) (dcabb39ab0b3); test(desktop): lock the Stop button to room.running and the stop primitive (b00e71dc931f); fmt(js): `npm run fix` on merge (#96263) (8d30c2044964)
- Затронутые файлы → куда смотреть в UI: plugins/hermes-bots/tests/group-chat-empty-sentinel.test.mjs + group-stop-thread.test.mjs (dcabb39ab0b3, b00e71dc931f) → только тесты, UI не меняют: поведение Stop-кнопки группового раунда и "(empty)" sentinel уже отслежены в 18:01; i18n/ar|ja|zh|zh-hant.ts + use-session-tile-delegate.ts + read-only-transcript.ts (8d30c2044964) → чистый `npm run fix` (#96263), en.ts не тронут — визуально смотреть нечего
- Новые ключи en.ts: нет изменений (EN_TS_SHA 64976a73cc86e9f0 — тот же, что в 12:01/14:02/18:01)
- Что проверить перед следующим релизом мода: ничего срочного — 3 коммита это тесты + форматирование, v0.20.6-роллап не добавляет desktop-строк; перенос с 18:01: «Stop this run — interrupts the member on turn and holds the rest» ×2 (plugin.js:13515/13553, вкладка «Боты» → тултип кнопки Stop раунда; в моде 0 совпадений) — перевести к следующему релизу. LITERALS_UNCOVERED=21 — набор тот же, новых нет

## 2026-08-28 00:01 (auto)
- Релизы: нет новых (v2026.8.27 от 27.08 записан 20:04; из окна per_page=5 выпал v2026.8.13 — те же 4 прочих)
- Коммиты apps/desktop: 5 новых с прошлого прогона (после 20:04; окно 15, 10 уже виденных в 18:01/20:04), темы: fix(desktop): unwrap Mistral Voxtral JSON in client-direct STT (bc737576ba); test(desktop): cover Voxtral JSON unwrap on client-direct STT (c086bb6f71); fix(desktop): retain remote owner after session resume (f54d015470); fix(desktop): recover cloud auth through portal (#96170) (46f091b93e); fmt(js): `npm run fix` on merge (#96506) (ca2a0d4d6f)
- Затронутые файлы → куда смотреть в UI: session-owner-stamp.ts + use-session-tile-delegate.ts + i18n/en.ts (9faa685385 #94724 — в окне с 18:01, но en.ts-изменение проявилось только сейчас) → загрузка сессий / сайдбар «Недавние»: старый чат, который не заявлен ни одним бэкендом, открывается как read-only транскрипт (баннер «Opened read-only», отправка заблокирована); client-direct STT, распаковка Mistral Voxtral JSON (bc737576ba) → голосовой ввод (Настройки → Голос, client-direct STT): поведение, строк нет; cloud auth через portal (46f091b93e #96170) → вход в облачный аккаунт (поведение)
- Новые ключи en.ts: readOnlyTranscriptTitle 'Opened read-only', readOnlyTranscriptBody 'No connected backend claims this older chat yet, so it opened as a read-only transcript…', readOnlyTranscriptSendBlocked 'This chat is open as a read-only transcript — sending is disabled.' (3 шт из 9faa685385; EN_TS_SHA bd6e252cbf4702fb, был 64976a73cc86e9f0). НЕ покрыты модом v1.2.1: 0 совпадений в i18n/ru.ts, registry.json, overrides.json
- Что проверить перед следующим релизом мода: 1) перевести readOnlyTranscript.* (загрузка сессий: баннер «Opened read-only» + блокировка отправки в чате без бэкенда); 2) вижн-тест: session resume сохраняет remote-владельца (f54d015470), client-direct STT корректно разбирает Voxtral-ответы; 3) LITERALS_UNCOVERED=21 — набор тот же (19 базы + «Stop this run» ×2), позиции не сдвинулись, новых нет

## 2026-08-28 02:03 (auto)
- Релизы: нет (те же 5, записаны 24.08 17:03/20:04: v2026.8.27 27.08, v2026.8.19 21.08, v2026.8.18 18.08, v2026.8.16.2 17.08, v2026.8.16 16.08)
- Коммиты apps/desktop: нет новых с прошлого прогона (окно 15 полностью совпадает с 00:01 — ca2a0d4d6f68…411f9c2f4404, те же 5 новых от 00:01 + 10 виденных ранее)
- Затронутые файлы → куда смотреть в UI: апстрим НЕ менялся (plugin.js на origin/main проверен: «Model switch failed» на 10145 и «Stop this run» на 13515/13553 на месте); единственный дельта — рабочее дерево мода: package/overrides.json +2 правила (hermes-bots-model-switch-failed, hermes-bots-stop-this-run all:true) → вкладка «Боты»: пикер модели (failureMessage «Не удалось переключить модель») и тултип кнопки Stop группового раунда («Остановить этот запуск — прерывает текущего участника и удерживает остальных», обе позиции 13515/13553) — переведены в WIP, ждут релиза
- Новые ключи en.ts: нет изменений (EN_TS_SHA bd6e252cbf4702fb совпадает с прогоном 00:01)
- Что проверить перед следующим релизом мода: ничего срочного из апстрима; перенос с 18:01/20:04/00:01 — «Stop this run» ×2 и «Model switch failed» уже покрыты в рабочем дереве (незакоммичено, проверено: readOnlyTranscript.* пока НЕ покрыт — 0 совпадений, остаётся следующим); вижн-тест: тултип Stop в групповом чате ботов и failureMessage пикера модели Bot Mode; LITERALS_UNCOVERED=21→18 — 3 литерала закрыты WIP-правилами мода, остальные 18 — прежний набор, позиции без изменений

## 2026-08-28 04:02 (auto)
- Релизы: нет (те же 5: v2026.8.27 27.08, v2026.8.19 21.08, v2026.8.18 18.08, v2026.8.16.2 17.08, v2026.8.16 16.08)
- Коммиты apps/desktop: 5 новых с прошлого прогона (после 02:03; окно 15, 10 виденных ранее — ca2a0d4d6f68…b00e71dc931f), темы: fix(desktop): keep bot chat focused when clicking the Bots pane (#96062) (253b9d78c); style: sort MINIMIZED_TRACK import (perfectionist lint) for salvaged #95956 (9a9e9074c); fix(hermes-bots): keep the Cronjobs tile registered while it holds focus in Bot Mode (dbca7a4f0); fix(desktop): keep a restore tab when a pane or strip collapses (#91223) (584f3a748); fix(desktop): gate transcript budget cap so Show earlier works (a24c12d14)
- Затронутые файлы → куда смотреть в UI: store/session-states.ts (253b9d78c #96062) → вкладка «Боты»: клик по панели «Боты» не уводит фокус из чата бота (поведение, строк нет); plugins/hermes-bots/plugin.js (dbca7a4f0) → вкладка «Боты» / Cronjobs: тайл Cronjobs остаётся зарегистрированным, пока держит фокус в Bot Mode (поведение; позиции литералов сдвинулись +7, напр. «New group conversations…» 15947→15954); components/pane-shell/tree/* (584f3a748 #91223) → вкладки/панели (⌘K, меню макетов, правый клик по зонам): при схлопывании панели или полосы остаётся restore-таб; components/assistant-ui/thread/list.tsx (a24c12d14) → сообщения ассистента: «Show earlier» больше не блокируется бюджет-капом транскрипта; tree-split.tsx (9a9e9074c) — чистый lint (порядок импорта), UI не меняет
- Новые ключи en.ts: нет изменений (EN_TS_SHA bd6e252cbf4702fb совпадает с 00:01/02:03)
- Что проверить перед следующим релизом мода: 1) вижн-тест: фокус чата бота при клике на панель «Боты» (#96062) и тайл Cronjobs в Bot Mode (dbca7a4f0) — вкладка «Боты»; 2) вижн-тест: restore-таб при схлопывании панели/полосы (#91223, вкладки/макеты); 3) вижн-тест: «Show earlier» в длинном транскрипте после бюджет-капа (a24c12d14); перенос с 00:01/02:03 — readOnlyTranscript.* всё ещё не покрыт (0 совпадений в registry/overrides/ru.ts), остаётся следующим переводом. LITERALS_UNCOVERED 18→17: закрыт «Name the bot first…» (plugin.js:10986) новым WIP-правилом overrides.json рабочего дерева мода (после релиза 1.2.1); остальные 17 — прежний набор, «New group conversations…» 15947→15954 (сдвиг от dbca7a4f0)

## 2026-08-28 (release note, вручную)

- Релиз **v1.2.2** (тестовый → подтверждён Владом → публичный): +35 i18n-ключей
  0.20.6 (managedUpdates, keychain, fleet, readOnlyTranscript, cron.modelImpact, pop*,
  openInExternal, Browser-раздел, Sidebar), +8 registry-правил (Activity-группа,
  Stop ×2, status-метки, плейсхолдер бота), фиксы: запятая ru-constants (краш
  сборки), переписаны якоря session-expired (2 новые формы), удалены 4 мёртвых
  правила + wake-word hint. Реестр: 946 → **953**. EXPECTED_COMMIT 39f1e1881a0.
  tsc-гейт `files/*.ts` в build-release-zip.py; `--allow-stale-dist` — честная
  диагностика без dist в поставке.
