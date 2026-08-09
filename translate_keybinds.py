#!/usr/bin/env python3
"""Перевод 93 keybinds-ключей (секция, пропущенная и warment) + повторный merge."""
import json

T = {}

def add(path, val):
    T[path] = val

# composer.hotkeyDescs (подписи в попапе — строчные)
add('composer.hotkeyDescs.composer.cancel', "'закрыть попап · отменить запуск'")
add('composer.hotkeyDescs.composer.help', "'эта справка (Delete — скрыть)'")
add('composer.hotkeyDescs.composer.history', "'переключение попапа / истории'")
add('composer.hotkeyDescs.composer.mention', "'упоминание файлов, папок, URL, git'")
add('composer.hotkeyDescs.composer.sendNewline', "'отправить · Shift+Enter — новая строка'")
add('composer.hotkeyDescs.composer.sendQueued', "'отправить следующий ход из очереди'")
add('composer.hotkeyDescs.composer.slash', "'палитра слэш-команд'")
add('composer.hotkeyDescs.keybinds.openPanel', "'все горячие клавиши'")

# keybinds.actions
add('keybinds.actions.appearance.toggleMode', "'Переключить светлую / тёмную тему'")
add('keybinds.actions.composer.cancel', "'Закрыть попап · отменить запуск'")
add('keybinds.actions.composer.focus', "'Фокус на поле ввода'")
add('keybinds.actions.composer.help', "'Быстрая справка'")
add('keybinds.actions.composer.history', "'Переключить попап / историю'")
add('keybinds.actions.composer.mention', "'Упомянуть файлы, папки, URL'")
add('keybinds.actions.composer.modelPicker', "'Открыть выбор модели'")
add('keybinds.actions.composer.newline', "'Вставить новую строку'")
add('keybinds.actions.composer.queue', "'Поставить сообщение в очередь'")
add('keybinds.actions.composer.send', "'Отправить сообщение'")
add('keybinds.actions.composer.sendQueued', "'Отправить следующий ход из очереди'")
add('keybinds.actions.composer.slash', "'Палитра слэш-команд'")
add('keybinds.actions.composer.steer', "'Направить текущий ход'")
add('keybinds.actions.composer.voice', "'Начать / остановить голосовой разговор'")
add('keybinds.actions.keybinds.openPanel', "'Открыть горячие клавиши'")
add('keybinds.actions.nav.agents', "'Открыть агентов'")
add('keybinds.actions.nav.artifacts', "'Открыть артефакты'")
add('keybinds.actions.nav.commandCenter', "'Открыть командный центр'")
add('keybinds.actions.nav.commandPalette', "'Открыть палитру команд'")
add('keybinds.actions.nav.cron', "'Открыть запланированные задачи'")
add('keybinds.actions.nav.messaging', "'Открыть мессенджеры'")
add('keybinds.actions.nav.profiles', "'Открыть профили'")
add('keybinds.actions.nav.settings', "'Открыть настройки'")
add('keybinds.actions.nav.skills', "'Открыть навыки'")
add('keybinds.actions.profile.create', "'Создать профиль'")
add('keybinds.actions.profile.default', "'Переключиться на профиль по умолчанию'")
add('keybinds.actions.profile.next', "'Следующий профиль'")
add('keybinds.actions.profile.prev', "'Предыдущий профиль'")
for n in range(1, 19):
    add(f'keybinds.actions.profile.switch.{n}', f"'Переключиться на профиль {n}'")
add('keybinds.actions.profile.toggleAll', "'Переключить вид всех профилей'")
add('keybinds.actions.session.focusSearch', "'Поиск сессий'")
add('keybinds.actions.session.new', "'Новая сессия'")
add('keybinds.actions.session.newTab', "'Новая вкладка сессии'")
add('keybinds.actions.session.newWindow', "'Новое окно'")
add('keybinds.actions.session.next', "'Следующая сессия'")
add('keybinds.actions.session.prev', "'Предыдущая сессия'")
for n in range(1, 10):
    add(f'keybinds.actions.session.slot.{n}', f"'Переключиться на недавнюю сессию {n}'")
add('keybinds.actions.session.togglePin', "'Закрепить / открепить текущую сессию'")
add('keybinds.actions.view.closeTab', "'Закрыть вкладку'")
add('keybinds.actions.view.closeTerminal', "'Закрыть терминал'")
add('keybinds.actions.view.findInPage', "'Найти на странице'")
add('keybinds.actions.view.findNext', "'Следующее совпадение'")
add('keybinds.actions.view.findPrevious', "'Предыдущее совпадение'")
add('keybinds.actions.view.flipPanes', "'Поменять стороны боковой панели'")
add('keybinds.actions.view.newTerminal', "'Новый терминал'")
add('keybinds.actions.view.nextTerminal', "'Следующий терминал'")
add('keybinds.actions.view.prevTerminal', "'Предыдущий терминал'")
add('keybinds.actions.view.reopenTab', "'Восстановить закрытую вкладку'")
add('keybinds.actions.view.showFiles', "'Показать обозреватель файлов'")
add('keybinds.actions.view.showTerminal', "'Переключить терминал'")
add('keybinds.actions.view.terminalCopy', "'Копировать выделение терминала'")
add('keybinds.actions.view.terminalPaste', "'Вставить в терминал'")
add('keybinds.actions.view.terminalSelection', "'Отправить выделение терминала в поле ввода'")
add('keybinds.actions.view.toggleHud', "'Переключить режим HUD'")
add('keybinds.actions.view.toggleReview', "'Переключить панель рецензирования'")
add('keybinds.actions.view.toggleRightSidebar', "'Переключить обозреватель файлов'")
add('keybinds.actions.view.toggleSidebar', "'Переключить боковую панель сессий'")
add('keybinds.actions.view.toggleStatusbar', "'Переключить строку состояния'")
add('keybinds.actions.workspace.newWorktree', "'Новый worktree'")
add('keybinds.actions.workspace.openFolder', "'Открыть папку как проект'")

print('переведено ключей:', len(T))
json.dump(T, open('/home/covhnw/projects/hermes-desktop-ru/translations_manual2.json', 'w'),
          ensure_ascii=False, indent=1)

# мержим в финальную таблицу и пере-merge
final = json.load(open('/home/covhnw/projects/hermes-desktop-ru/translations_final.json'))
before = len(final)
final.update(T)
json.dump(final, open('/home/covhnw/projects/hermes-desktop-ru/translations_final.json', 'w'),
          ensure_ascii=False)
print(f'финальная таблица: {before} → {len(final)}')
