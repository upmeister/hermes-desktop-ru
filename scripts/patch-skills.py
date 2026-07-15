#!/usr/bin/env python3
"""Patch skills/index.tsx to add Russian description translations."""
import os
import sys

SKILL_DESC_BLOCK = '''// Russian translations for known skill descriptions
const SKILL_DESC_RU: Record<string, string> = {
  'apple-notes': 'Управление Apple Notes через memo CLI: создание, поиск, редактирование.',
  'apple-reminders': 'Apple Reminders через remindctl: добавление, просмотр, выполнение.',
  'findmy': 'Отслеживание устройств Apple/AirTags через FindMy.app на macOS.',
  'imessage': 'Отправка и получение iMessages/SMS через imsg CLI на macOS.',
  'macos-operations': 'Полная поддержка системы и приложений macOS: автоматизация рабочего стола, диагностика, интеграции Apple (Notes, Reminders, FindMy, Messages), общие паттерны CLI.',
  'claude-code': 'Делегирование кодирования Claude Code CLI (фичи, PR).',
  'hermes-agent': 'Настройка, расширение или вклад в Hermes Agent.',
  'opencode': 'Делегирование кодирования OpenCode CLI (фичи, обзор PR).',
}

function localizedDescription(skill: { description?: string | Record<string, string> }, locale: string): string {
  if (locale !== 'ru') return asText(skill.description)
  const name = asText((skill as { name?: string }).name ?? '')
  return SKILL_DESC_RU[name] || asText(skill.description)
}
'''

LOCALIZED_DESC_LINE = '{localizedDescription(skill, locale) || t.skills.noDescription}'


def patch(hermes_dir):
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/skills/index.tsx')

    if not os.path.exists(filepath):
        print(f"  [!] File not found: {filepath}")
        return False

    with open(filepath, 'r') as f:
        content = f.read()

    # Check if already patched
    if 'SKILL_DESC_RU' in content:
        print("  [~] skills/index.tsx already patched")
        return True

    # Add locale to useI18n destructuring
    content = content.replace(
        "const { t } = useI18n()",
        "const { t, locale } = useI18n()"
    )

    # Insert SKILL_DESC_BLOCK before the component
    marker = "const SKILLS_MODES"
    if marker in content:
        content = content.replace(marker, SKILL_DESC_BLOCK + "\n" + marker)

    # Replace skill description rendering
    content = content.replace(
        '{asText(skill.description) || t.skills.noDescription}',
        LOCALIZED_DESC_LINE
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print("  [✓] skills/index.tsx patched")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: patch-skills.py <hermes-dir>")
        sys.exit(1)

    patch(sys.argv[1])