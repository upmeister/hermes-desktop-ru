#!/usr/bin/env python3
"""plans-view.tsx: хардкод → t()/translateNow."""
path = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/app/settings/billing/plans-view.tsx'
src = open(path, encoding='utf-8').read()

fixes = [
    ("import { Button } from '@/components/ui/button'",
     "import { Button } from '@/components/ui/button'\nimport { translateNow, useI18n } from '@/i18n'"),
    # previewMessage через translateNow
    ("""function previewMessage(phase: DowngradePhase, fallbackTierName: string): null | string {
  if (phase.kind === 'previewing') {
    return 'Checking this change…'
  }""",
     """function previewMessage(phase: DowngradePhase, fallbackTierName: string): null | string {
  if (phase.kind === 'previewing') {
    return translateNow('settings.billingPage.checkingChange')
  }"""),
    ("      return preview.reason ?? 'That change cannot be made here.'",
     "      return preview.reason ?? translateNow('settings.billingPage.cannotChange')"),
    ("      return `You are already on ${targetName} — nothing to change.`",
     "      return translateNow('settings.billingPage.alreadyOnPlan', targetName)"),
    ("""      return (
        `Change to ${targetName} — takes effect ${formatBillingDate(preview.effective_at)}. No charge now; ` +
        `you keep your current plan until then.${creditsDelta ? ` Monthly credits change: ${creditsDelta}.` : ''}`
      )""",
     "      return translateNow('settings.billingPage.changeTakesEffect', targetName, formatBillingDate(preview.effective_at), creditsDelta)"),
    ("      return 'This change cannot be scheduled here.'",
     "      return translateNow('settings.billingPage.cannotSchedule')"),
    # DowngradeConfirm: хук
    ("function DowngradeConfirm({ flow, tier }: { flow: DowngradeFlow; tier: BillingPlanTierView }) {\n  const active = flow.active",
     "function DowngradeConfirm({ flow, tier }: { flow: DowngradeFlow; tier: BillingPlanTierView }) {\n  const { t } = useI18n()\n  const active = flow.active"),
    ("            Try again\n", "            {t.settings.billingPage.tryAgain}\n"),
    ("""            {phase.kind === 'scheduling'
              ? 'Scheduling…'
              : phase.kind === 'scheduleFailed'
                ? 'Try again'
                : 'Confirm downgrade'}""",
     """            {phase.kind === 'scheduling'
              ? t.settings.billingPage.scheduling
              : phase.kind === 'scheduleFailed'
                ? t.settings.billingPage.tryAgain
                : t.settings.billingPage.confirmDowngrade}"""),
    ("          Cancel\n", "          {t.common.cancel}\n"),
    # PlanCard: хук
    ("function PlanCard({ flow, tier }: { flow: DowngradeFlow; tier: BillingPlanTierView }) {\n  const isCurrent = tier.state === 'current'",
     "function PlanCard({ flow, tier }: { flow: DowngradeFlow; tier: BillingPlanTierView }) {\n  const { t } = useI18n()\n  const isCurrent = tier.state === 'current'"),
    ("        {isCurrent && <Pill tone=\"primary\">Current plan</Pill>}",
     "        {isCurrent && <Pill tone=\"primary\">{t.settings.billingPage.currentPlan}</Pill>}"),
    ("        {tier.state === 'scheduled' && <Pill>Scheduled</Pill>}",
     "        {tier.state === 'scheduled' && <Pill>{t.settings.billingPage.scheduled}</Pill>}"),
    ("              Downgrade\n", "              {t.settings.billingPage.downgrade}\n"),
    # BillingPlansView: хук
    ("export function BillingPlansView({ onBack, tiers }: { onBack: () => void; tiers: BillingPlanTierView[] }) {\n  // A scheduled downgrade",
     "export function BillingPlansView({ onBack, tiers }: { onBack: () => void; tiers: BillingPlanTierView[] }) {\n  const { t } = useI18n()\n  // A scheduled downgrade"),
    ('aria-label="Back to billing"', 'aria-label={t.settings.billingPage.backToBilling}'),
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
