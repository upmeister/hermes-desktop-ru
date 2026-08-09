#!/usr/bin/env python3
"""custom-endpoints, appearance-settings, combobox-input → t()."""
BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/app/settings/'

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
    print(f'записано: {path}\n')

apply(BASE + 'custom-endpoints-settings.tsx', [
    # найти первый '@/'-импорт для вставки useI18n
    ("import { Button } from '@/components/ui/button'",
     "import { Button } from '@/components/ui/button'\nimport { useI18n } from '@/i18n'"),
    ("                      title=\"Delete endpoint\"",
     "                      title={t.settings.endpoints.deleteAria}"),
    ('<EmptyState description="Add an OpenAI-compatible endpoint below." title="No custom endpoints" />',
     '<EmptyState description={t.settings.endpoints.emptyDesc} title={t.settings.endpoints.emptyTitle} />'),
    ("<SectionHeading icon={Plus} title={form.id ? 'Edit Endpoint' : 'Add Endpoint'} />",
     "<SectionHeading icon={Plus} title={form.id ? t.settings.endpoints.edit : t.settings.endpoints.add} />"),
    ("{endpoint.has_api_key && <span>{endpoint.api_key_preview ?? 'API key set'}</span>}",
     "{endpoint.has_api_key && <span>{endpoint.api_key_preview ?? t.settings.endpoints.apiKeySet}</span>}"),
])

apply(BASE + 'combobox-input.tsx', [
    ("import { Check, ChevronDown } from '@/lib/icons'",
     "import { Check, ChevronDown } from '@/lib/icons'\nimport { useI18n } from '@/i18n'"),
])
