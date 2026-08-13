import { useAuiState } from '@assistant-ui/react'
import { useI18n } from '@/i18n'
import { formatAgo } from '@/lib/time'
import { cn } from '@/lib/utils'
import { formatMessageTimestamp } from '@/components/assistant-ui/thread/timestamp'

// Mod: hermes-desktop-timestamps — always-visible message timestamp.
// Stock shows the age only inside the hover-revealed action bar (MessageAge),
// and user messages have no time at all. This component renders the timestamp
// (Today/Yesterday/full date) with the relative age as a hover title.
export function MessageTimestamp({ className }: { className?: string }) {
  // NOTE (13.08): useI18n() returns I18nContextValue ({ t, locale, ... }) in
  // the new i18n architecture (v0.20) — MUST destructure. The old API
  // (v0.17) returned the translations object directly; this was the cause of
  // the "workspace failed to render: Cannot read properties of undefined
  // (reading 'thread')" crash on user messages.
  const { t } = useI18n()
  const createdAt = useAuiState(s => s.message.createdAt)
  if (!createdAt) return null
  const date = new Date(createdAt)
  const label = formatMessageTimestamp(date, t.assistant.thread) || undefined
  return (
    <span
      className={cn('px-0.5 text-[0.6875rem] tabular-nums text-muted-foreground', className)}
      title={formatAgo(date.getTime(), t.agents)}
    >
      {label}
    </span>
  )
}
