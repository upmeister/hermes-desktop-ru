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

## 2026-08-22 22:00 (auto)
- Релизы: v2026.8.19 (2026-08-21), v2026.8.18 (2026-08-18), v2026.8.16.2 (2026-08-17), v2026.8.16 (2026-08-16), v2026.8.13 (2026-08-13)
- Коммиты apps/desktop: 15 штук. Первые 5: fix(bot-mode): persist canonical chat before opening; fix(bot-mode): canonical Bot Chat ищется по NAME (session-id pins удалены); fix(tests): четыре shared-state/lifetime бага при высокой конкуренции; ci: work lanes на больших раннерах; fix(bot-mode): строка бота открывает canonical Bot Chat (#92042). Также: feat(desktop): Send Diagnostics — одно-клик загрузка редактированного debug-бандла из error-карточки + review-фиксы (0a9a449a32e7), fix(desktop): strip off-scheme paint из selection copies (3cc7f220cdd2).
- Новые ключи en.ts: первый прогон — базлайн, сравнения с прошлой версией нет. Актуальный SHA 9712c9e5e334c551. Desktop-секции на месте: sendDiagnostics (1271 знаков: title/privacyNotice/upload/uploading/cancel…), updates (стадии idle/prepare/fetch/pull/pydeps/update/rebuild/restart/done/manual/guiSkew/error, checking, checkFailedTitle, notAvailableTitle…), billingBlock (titleNous/titleProvider/fallbackMessage/openBilling/addCredits/dismiss), titlebar, keybinds, findInPage, language, settings, onboarding, modelPicker, shell, rightSidebar, errors, ui.
- Что проверить перед следующим релизом мода: 1) новые ключи секции sendDiagnostics (фича из 8f30e9c77a9e) — нужен ли перевод в ru-mod; 2) EXPECTED_COMMIT и apply-hardcodes.mjs против апстрима на теге v2026.8.19 (релиз свежее последнего baseline); 3) fix(desktop) 3cc7f220cdd2 (strip off-scheme paint) — проверить, не затронуты ли патчем строки правок.

## 2026-08-23 02:05 (auto)
- Релизы: нет (те же 5, что в записи 22:00: v2026.8.19/18/16.2/16/13)
- Коммиты apps/desktop: 4 новых с прошлого прогона (state 00:01): 4b860d8193ff `fmt(js): npm run fix` #92399; 67a5d7bcf0b3 fix(desktop) — Win10 translucency берётся из платформы, а не glass-capability; 40f3e58f6de9 fix(desktop) — остановить производство дублей toolCallId на фолде, починка отравленных кэш-хвостов; 9f8dca34dc2a fix(desktop) — дедуп toolCallId-частей на runtime-границе (#87857). Из топ-15 выпали: 8286c46502e1, 3cc7f220cdd2, 729782d058e6, be98423fe159.
- Новые ключи en.ts: нет изменений (content-SHA 9712c9e5e334c551 — совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: ничего срочного — i18n не затронут (новые коммиты — рантайм/оконные фиксы, строк не добавляют); при следующем релизе переснять EXPECTED_COMMIT против актуального main (сейчас мод на 14c59f0b505).

## 2026-08-23 (release note, вручную)
- Релиз **v1.0.5**: +5 правил (тосты ботов/реакций, api/client.ts), ru.ts updates-секция
  (applyingBody/Backend, guiSkewBody, +7 ключей), скрин bots+kanban заменён. Registry 647.
  EXPECTED_COMMIT прежний `987064caa4f` (апстрим не двигался).
- Правило с 1.0.4: при каждом релизе дописывать сюда строку-фиксу (формат выше), чтобы журнал не врал на итерацию.

## 2026-08-23 12:03 (auto)
- Релизы: нет (те же 5: v2026.8.19/18/16.2/16/13 — 21.08/18.08/17.08/16.08/13.08)
- Коммиты apps/desktop: 4 новых с прошлого прогона (state 04:01): c942cd9ea143 fix(desktop) — settings scope requests не могут случайно целиться в primary; abd7f75b8d07 fix(desktop) — держать Messaging на активном профиле; 680b11503cbf fix(desktop) — настройки модели следуют активному профилю, а не primary; 87b645f52ccc fix(desktop) — неудачный lookup Bot Chat registry больше не форкает вечный чат бота
- Новые ключи en.ts: нет изменений (content-SHA 9712c9e5e334c551 — совпадает с прошлым прогоном)
- Что проверить перед следующим релизом мода: ничего срочного — i18n не затронут; все 4 коммита — рантайм-фиксы мульти-профильной маршрутизации (settings/Messaging/model по активному профилю), UI-строк не добавляют; отдельно: 38ce2d7553c4 «enforce exact route identity authority» прилетел сразу после снапшота (та же тема — идентичность маршрута) — взять в следующий тик.