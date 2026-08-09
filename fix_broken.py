#!/usr/bin/env python3
"""Фикс 15 битых значений: переводы + добавление в таблицу и override."""
import json

FIXES = {
    'messaging.pendingAria':
        "count => `${count} ${count === 1 ? 'запрос' : 'запросов'} на сопряжение`",
    'messaging.revokeDesc':
        "(name: string) => `${name} потеряет доступ и перестанет распознаваться со следующего сообщения.`",
    'settings.config.attachmentSizeDesc':
        "'Насколько большой локальный файл Desktop загрузит для предпросмотра и вложений изображений, в МБ. По умолчанию 16. Для удалённых вложений не-изображений действует отдельный лимит 256 МБ. Очень высокое значение загружает файл целиком в память и может заморозить или уронить приложение.'",
    'settings.config.keepAwakeDesc':
        "'Не давать этой машине засыпать, чтобы длительные или ночные запуски продолжали работать. Экран при этом может гаснуть.'",
    'settings.gateway.sshDesc':
        "'Hermes запускается на удалённой машине по SSH и туннелируется в это приложение — ничего не нужно запускать или открывать самому. Требуется рабочий доступ к хосту по SSH-ключам.'",
    'settings.gateway.sshErrAuth':
        "'Ошибка аутентификации SSH. Загрузите ключ в ssh-agent (ssh-add) или укажите IdentityFile в ~/.ssh/config — Hermes запускает ssh в неинтерактивном режиме.'",
    'settings.gateway.sshErrHostKey':
        "'Ключ хоста ИЗМЕНИЛСЯ с момента последнего подключения. Убедитесь, что это ожидаемо, затем выполните ssh-keygen -R <host> и подключитесь снова.'",
    'settings.gateway.sshErrNotInstalled':
        "'Hermes не установлен на удалённом хосте. Установите его там (curl -fsSL https://hermes-agent.nousresearch.com/install.sh | sh) или укажите путь к Hermes.'",
    'settings.gateway.sshErrPlatform':
        "'Неподдерживаемая платформа удалённого хоста. Режим SSH в Hermes Desktop поддерживает Linux, macOS и Windows.'",
    'settings.gateway.sshReachable':
        "(host, platform) => `Доступен: ${host} (${platform}) — Hermes найден`",
    'settings.gateway.sshTrustHint':
        "'Первый представленный ключ хоста доверяется и закрепляется; последующие изменения приводят к отказу.'",
    'settings.sessions.autoArchiveDesc':
        "\"Автоматически архивировать чаты, к которым вы давно не обращались. Закреплённые чаты никогда не архивируются, ничего не удаляется — архивированные чаты просто перемещаются сюда.\"",
    'settings.toolsets.nousAuthNeededMessage':
        "provider => `${provider} сохранён, но не активируется, пока вы не войдёте в Nous Portal.`",
    'settings.toolsets.terminalBackend.selectedMessage':
        "backend => `Команды терминала теперь выполняются через ${backend}. Применяется к новым сессиям.`",
    'settings.toolsets.webCapabilitySelectedMessage':
        "(provider, capability) => `${provider} теперь обрабатывает web ${capability}.`",
}

final = json.load(open('/home/covhnw/projects/hermes-desktop-ru/translations_final.json'))
override = json.load(open('/home/covhnw/projects/hermes-desktop-ru/translations_override.json'))

for p, v in FIXES.items():
    final[p] = v
    if p not in override:
        override.append(p)

json.dump(final, open('/home/covhnw/projects/hermes-desktop-ru/translations_final.json', 'w'), ensure_ascii=False)
json.dump(override, open('/home/covhnw/projects/hermes-desktop-ru/translations_override.json', 'w'), ensure_ascii=False, indent=1)
print(f'исправлено: {len(FIXES)}, override теперь: {len(override)}')
