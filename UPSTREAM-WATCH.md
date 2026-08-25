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