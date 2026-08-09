#!/usr/bin/env python3
"""auto-reload-row.tsx: хардкод → t()."""
path = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/app/settings/billing/auto-reload-row.tsx'
src = open(path, encoding='utf-8').read()

fixes = [
    ("import { Button } from '@/components/ui/button'",
     "import { Button } from '@/components/ui/button'\nimport { useI18n } from '@/i18n'"),
    ("""  const api = useBillingApi()
  const queryClient = useQueryClient()""",
     """  const { t } = useI18n()
  const api = useBillingApi()
  const queryClient = useQueryClient()"""),
    ("setMessage({ kind: 'success', text: 'Auto-refill updated.' })",
     "setMessage({ kind: 'success', text: t.settings.billingPage.autoRefillUpdated })"),
    ("setMessage({ kind: 'success', text: 'Auto-refill turned off.' })",
     "setMessage({ kind: 'success', text: t.settings.billingPage.autoRefillTurnedOff })"),
    ("                  Threshold\n", "                  {t.settings.billingPage.autoRefillThreshold}\n"),
    ('aria-label="Auto-refill threshold"', 'aria-label={t.settings.billingPage.autoRefillThresholdAria}'),
    ("                  Reload to\n", "                  {t.settings.billingPage.autoRefillReloadTo}\n"),
    ('aria-label="Auto-refill reload-to amount"', 'aria-label={t.settings.billingPage.autoRefillReloadToAria}'),
    ("                  <span>Turn off auto-refill?</span>",
     "                  <span>{t.settings.billingPage.turnOffAutoRefill}</span>"),
    ("                    Turn off\n", "                    {t.settings.billingPage.turnOff}\n"),
    ("                    Cancel\n", "                    {t.common.cancel}\n"),
    ("                  Disable\n", "                  {t.settings.billingPage.turnOff}\n"),
    ("                {busy ? 'Saving…' : 'Save'}", "                {busy ? t.common.saving : t.common.save}"),
    ("                Cancel\n", "                {t.common.cancel}\n"),
]

for old, new in fixes:
    n = src.count(old)
    if n != 1:
        print(f'ПРОПУЩЕНО ({n}): {old[:70]!r}')
        continue
    src = src.replace(old, new)
    print(f'ok: {old[:55]!r}')

open(path, 'w', encoding='utf-8').write(src)
print('записано')
