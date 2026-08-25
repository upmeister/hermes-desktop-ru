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
