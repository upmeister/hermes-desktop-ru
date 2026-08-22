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