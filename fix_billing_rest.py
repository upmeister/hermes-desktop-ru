#!/usr/bin/env python3
"""billing: index.tsx, inline-feedback.tsx, current-plan-card.tsx → t()."""
import sys

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

BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/app/settings/billing/'

# inline-feedback.tsx
apply(BASE + 'inline-feedback.tsx', [
    ("import { Button } from '@/components/ui/button'",
     "import { Button } from '@/components/ui/button'\nimport { useI18n } from '@/i18n'"),
    ("export function StepUpInlineAction({ flow }: { flow: ReturnType<typeof useStepUpFlow> }) {\n  if (flow.verification) {",
     "export function StepUpInlineAction({ flow }: { flow: ReturnType<typeof useStepUpFlow> }) {\n  const { t } = useI18n()\n  if (flow.verification) {"),
    ("          Open verification page\n", "          {t.settings.billingPage.openVerificationPage}\n"),
    ("    return <span>Waiting for verification link…</span>",
     "    return <span>{t.settings.billingPage.waitingForVerification}</span>"),
    ("      Verify to continue\n", "      {t.settings.billingPage.verifyToContinue}\n"),
])

# current-plan-card.tsx
apply(BASE + 'current-plan-card.tsx', [
    ("export function CurrentPlanCard({ onViewPlans, plan }: { onViewPlans: () => void; plan: BillingPlanCardView }) {",
     "export function CurrentPlanCard({ onViewPlans, plan }: { onViewPlans: () => void; plan: BillingPlanCardView }) {\n  const { t } = useI18n()"),
    ("              {resumeFlow.busy ? 'Undoing…' : 'Undo'}",
     "              {resumeFlow.busy ? t.settings.billingPage.undoing : 'Undo'}"),
])
