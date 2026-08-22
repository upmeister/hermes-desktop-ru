# Changelog

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).
Версии мода не совпадают 1:1 с версиями Hermes Desktop.

> Нумерация начата с 1.0.0 — это первый стабильный публичный релиз.
> Предыдущая линия 7.6.x (август 2026) считается тестовой и здесь не описывается;
> её историю можно посмотреть в git-истории репозитория.

## [Unreleased]

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
