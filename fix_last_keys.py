#!/usr/bin/env python3
"""9 недостающих ключей: переводы в таблицу/override + merge + замены в файлах."""
import json, subprocess

BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/'

# 1. таблица + override
final = json.load(open('/home/covhnw/projects/hermes-desktop-ru/translations_final.json'))
override = json.load(open('/home/covhnw/projects/hermes-desktop-ru/translations_override.json'))
ru = {
    'settings.billingPage.manage': "'Управлять'",
    'settings.billingPage.noPlansAvailable': "'Сейчас нет тарифов, на которые можно перейти.'",
    'settings.billingPage.plans': "'Тарифы'",
    'settings.billingPage.undo': "'Отменить'",
    'common.dismiss': "'Закрыть'",
    'common.toggleLogs': "'Переключить журналы'",
    'common.use': "'Использовать'",
    'settings.uninstall.checkingInstalled': "'Проверка установленного…'",
    'commandCenter.generatePet.setupImageGeneration': "'Настроить генерацию изображений'",
}
for p, v in ru.items():
    final[p] = v
    if p not in override:
        override.append(p)
json.dump(final, open('/home/covhnw/projects/hermes-desktop-ru/translations_final.json', 'w'), ensure_ascii=False)
json.dump(override, open('/home/covhnw/projects/hermes-desktop-ru/translations_override.json', 'w'), ensure_ascii=False, indent=1)
print('таблица: +9')

# 2. merge ru.ts
subprocess.run(['python3', '/home/covhnw/projects/hermes-desktop-ru/merge_locale_linux.py'], check=True)
import shutil
shutil.copy('/home/covhnw/projects/hermes-desktop-ru/i18n/ru.ts', BASE + 'i18n/ru.ts')
print('ru.ts пересобран')

# 3. замены в компонентах
def apply(path, fixes):
    src = open(path, encoding='utf-8').read()
    for old, new in fixes:
        n = src.count(old)
        if n != 1:
            print(f'ПРОПУЩЕНО ({n}): {old[:70]!r}')
            continue
        src = src.replace(old, new)
        print(f'ok: {old[:55]!r}')
    open(path, 'w', encoding='utf-8').write(src)

apply(BASE + 'app/settings/billing/auto-reload-row.tsx', [
    ("              Manage\n", "              {t.settings.billingPage.manage}\n"),
])
apply(BASE + 'app/settings/billing/plans-view.tsx', [
    ("        <span>Plans</span>", "        <span>{t.settings.billingPage.plans}</span>"),
    ("          No plans are available to change to right now.",
     "          {t.settings.billingPage.noPlansAvailable}"),
])
apply(BASE + 'app/settings/billing/current-plan-card.tsx', [
    ("{resumeFlow.busy ? t.settings.billingPage.undoing : 'Undo'}",
     "{resumeFlow.busy ? t.settings.billingPage.undoing : t.settings.billingPage.undo}"),
])
apply(BASE + 'app/settings/billing/inline-feedback.tsx', [
    ("          Dismiss\n", "          {t.common.dismiss}\n"),
])
apply(BASE + 'app/settings/uninstall-section.tsx', [
    ("            Checking what&apos;s installed…",
     "            {t.settings.uninstall.checkingInstalled}"),
])
apply(BASE + 'app/contrib/controller.tsx', [
    ("    label: 'Toggle logs',", "    label: translateNow('common.toggleLogs'),"),
])
apply(BASE + 'app/settings/custom-endpoints-settings.tsx', [
    ("                      Use\n", "                      {t.common.use}\n"),
])
apply(BASE + 'app/pet-generate/components/generate-unavailable.tsx', [
    ("        Set up image generation\n", "        {t.commandCenter.generatePet.setupImageGeneration}\n"),
])
print('все замены выполнены')
