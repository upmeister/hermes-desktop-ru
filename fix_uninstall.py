#!/usr/bin/env python3
"""uninstall-section.tsx: перенос OPTIONS в компонент + t()."""
path = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/app/settings/uninstall-section.tsx'
src = open(path, encoding='utf-8').read()

fixes = [
    # import
    ("import { Button } from '@/components/ui/button'",
     "import { Button } from '@/components/ui/button'\nimport { useI18n } from '@/i18n'"),
    # удаляем модульный OPTIONS
    ("""const OPTIONS: ModeOption[] = [
  {
    mode: 'gui',
    title: 'Uninstall Chat GUI only',
    description: 'Remove this desktop app. The Hermes agent, your config, and chats all stay.',
    consequence: 'the desktop Chat GUI (this app and its data)',
    needsAgent: false
  },
  {
    mode: 'lite',
    title: 'Uninstall GUI + agent, keep my data',
    description: 'Remove the app and the Hermes agent, but keep config, chats, and secrets for a future reinstall.',
    consequence: 'the Chat GUI and the Hermes agent (config, chats, and secrets are kept)',
    needsAgent: true
  },
  {
    mode: 'full',
    title: 'Uninstall everything',
    description: 'Remove the app, the agent, and all user data — config, chats, scheduled jobs, secrets, logs.',
    consequence: 'EVERYTHING — the Chat GUI, the Hermes agent, and all of your config, chats, secrets, and logs',
    // full removes the agent (and user data), so it's an agent-removing option:
    // hide it on a lite client with no local agent, same as lite. A lite client
    // connecting to a remote backend has no local agent OR local user data the
    // GUI installed, so gui-only is the correct (and only) option there.
    needsAgent: true
  }
]

""", ""),
    # хук + OPTIONS в компоненте
    ("export function UninstallSection() {\n  const [summary, setSummary] = useState<DesktopUninstallSummary | null>(null)",
     """export function UninstallSection() {
  const { t } = useI18n()
  const [summary, setSummary] = useState<DesktopUninstallSummary | null>(null)"""),
    # OPTIONS (внутри компонента) — вставить перед useEffect
    ("""  const [error, setError] = useState<string | null>(null)

  useEffect(() => {""",
     """  const [error, setError] = useState<string | null>(null)

  const OPTIONS: ModeOption[] = [
    {
      mode: 'gui',
      title: t.settings.uninstall.optionGui,
      description: t.settings.uninstall.optionGuiDesc,
      consequence: t.settings.uninstall.optionGuiConsequence,
      needsAgent: false
    },
    {
      mode: 'lite',
      title: t.settings.uninstall.optionLite,
      description: t.settings.uninstall.optionLiteDesc,
      consequence: t.settings.uninstall.optionLiteConsequence,
      needsAgent: true
    },
    {
      mode: 'full',
      title: t.settings.uninstall.optionFull,
      description: t.settings.uninstall.optionFullDesc,
      consequence: t.settings.uninstall.optionFullConsequence,
      // full removes the agent (and user data), so it's an agent-removing option:
      // hide it on a lite client with no local agent, same as lite. A lite client
      // connecting to a remote backend has no local agent OR local user data the
      // GUI installed, so gui-only is the correct (and only) option there.
      needsAgent: true
    }
  ]

  useEffect(() => {"""),
    # строки JSX
    ("setError(result.message || result.error || 'Uninstall could not start.')",
     "setError(result.message || result.error || t.settings.uninstall.couldNotStart)"),
    ('<SectionHeading icon={AlertTriangle} title="Danger zone" />',
     '<SectionHeading icon={AlertTriangle} title={t.settings.uninstall.heading} />'),
    ("            <p className=\"text-sm font-medium text-destructive\">Confirm uninstall</p>",
     "            <p className=\"text-sm font-medium text-destructive\">{t.settings.uninstall.confirmTitle}</p>"),
    ("              This removes {pendingOption.consequence}. This can&apos;t be undone.",
     "              {t.settings.uninstall.confirmDesc(pendingOption.consequence)}"),
    ("App: {summary.running_app_path}", "{t.settings.uninstall.appPath(summary.running_app_path)}"),
    ("                {running ? 'Uninstalling…' : 'Yes, uninstall'}",
     "                {running ? t.settings.uninstall.uninstalling : t.settings.uninstall.yes}"),
    ("                Cancel\n", "                {t.common.cancel}\n"),
    ("            <p className=\"text-sm font-medium\">Uninstall Hermes</p>",
     "            <p className=\"text-sm font-medium\">{t.settings.uninstall.title}</p>"),
    ("              Choose how much to remove. The app closes to finish the job; reopen the installer any time to come back.",
     "              {t.settings.uninstall.intro}"),
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
