#!/usr/bin/env python3
"""computer-use-panel.tsx: 20 хардкод-строк → t()."""
import sys

path = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/app/settings/computer-use-panel.tsx'
src = open(path, encoding='utf-8').read()

fixes = [
    # import
    ("import { Button } from '@/components/ui/button'",
     "import { Button } from '@/components/ui/button'\nimport { useI18n } from '@/i18n'"),
    # PLATFORM_NOTE константа — удаляем (перевод через t в компоненте)
    ("""// Per-OS one-liner shown when there's no TCC grant flow (Windows/Linux). macOS
// drives the permission rows instead, so it has no entry here.
const PLATFORM_NOTE: Record<string, string> = {
  linux: 'Drives your desktop via the X11/XWayland accessibility stack — no permission prompt.',
  win32: 'First run may trigger a Windows SmartScreen prompt for the cua-driver UIAccess worker — allow it.'
}

""", ""),
    # PermissionRow: хук + статусы
    ("function PermissionRow({ granted, label, hint }: { granted: boolean | null; label: string; hint: string }) {\n  return (",
     "function PermissionRow({ granted, label, hint }: { granted: boolean | null; label: string; hint: string }) {\n  const { t } = useI18n()\n  return ("),
    ("{granted === true ? 'Granted' : granted === false ? 'Not granted' : 'Unknown'}",
     "{granted === true ? t.settings.computerUse.granted : granted === false ? t.settings.computerUse.notGranted : t.settings.computerUse.unknown}"),
    # ComputerUsePanel: хук
    ("export function ComputerUsePanel({ onConfiguredChange }: ComputerUsePanelProps) {\n  const [status, setStatus] = useState<ComputerUseStatus | null>(null)",
     "export function ComputerUsePanel({ onConfiguredChange }: ComputerUsePanelProps) {\n  const { t } = useI18n()\n  const [status, setStatus] = useState<ComputerUseStatus | null>(null)"),
    ("notifyError(err, 'Could not read Computer Use status')",
     "notifyError(err, t.settings.computerUse.errorRead)"),
    ("notifyError(new Error('spawn failed'), 'Could not request permissions')",
     "notifyError(new Error('spawn failed'), t.settings.computerUse.errorRequest)"),
    ("        title: 'Approve in System Settings',\n        message: 'macOS will show a permission dialog attributed to CuaDriver. Approve it, then return here.'",
     "        title: t.settings.computerUse.approveTitle,\n        message: t.settings.computerUse.approveMessage"),
    ("        notifyError(err, 'Could not request permissions')",
     "        notifyError(err, t.settings.computerUse.errorRequest)"),
    ("        Checking Computer Use status…",
     "        {t.settings.computerUse.checking}"),
    ("        Computer Use isn&apos;t supported on this platform ({status.platform}).",
     "        {t.settings.computerUse.notSupported(status.platform)}"),
    ("        Install the cua-driver backend below to drive this machine.\n        {status.can_grant && ' Then grant Accessibility and Screen Recording here.'}",
     "        {t.settings.computerUse.notInstalled}\n        {status.can_grant && t.settings.computerUse.notInstalledGrant}"),
    ("""              Grants attach to CuaDriver&apos;s own identity (com.trycua.driver), not Hermes — so the dialog is
              attributed to the process that drives your Mac.""",
     "              {t.settings.computerUse.grantsNote}"),
    ("            <p className=\"text-[0.72rem] text-muted-foreground\">{PLATFORM_NOTE[status.platform] ?? ''}</p>",
     "            <p className=\"text-[0.72rem] text-muted-foreground\">{status.platform === 'linux' ? t.settings.computerUse.platformNoteLinux : t.settings.computerUse.platformNoteWin}</p>"),
    ("          Recheck\n", "          {t.settings.computerUse.recheck}\n"),
    ("            hint=\"Lets cua-driver post clicks, keystrokes, and read the accessibility tree.\"\n            label=\"Accessibility\"",
     "            hint={t.settings.computerUse.accessibilityHint}\n            label={t.settings.computerUse.accessibility}"),
    ("            hint=\"Lets cua-driver capture screenshots of app windows.\"\n            label=\"Screen Recording\"",
     "            hint={t.settings.computerUse.screenRecordingHint}\n            label={t.settings.computerUse.screenRecording}"),
    ("          <span className=\"text-sm font-medium\">Driver health</span>",
     "          <span className=\"text-sm font-medium\">{t.settings.computerUse.driverHealth}</span>"),
    ("            {status.ready === true ? 'Ready' : status.ready === false ? 'Not ready' : 'Unknown'}",
     "            {status.ready === true ? t.settings.computerUse.ready : status.ready === false ? t.settings.computerUse.notReady : t.settings.computerUse.unknown}"),
    ("          Computer Use is ready. Ask the agent to capture an app and click around.",
     "          {t.settings.computerUse.readyMessage}"),
    ("            {granting ? 'Waiting for approval…' : 'Grant permissions'}",
     "            {granting ? t.settings.computerUse.waitingApproval : t.settings.computerUse.grantPermissions}"),
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
