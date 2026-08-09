#!/usr/bin/env python3
"""Группа 3: controller, index.tsx, quick-entry, pet-generate, pet-overlay."""
BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/'

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

# controller.tsx — модульный код → translateNow
apply(BASE + 'app/contrib/controller.tsx', [
    ("    title: 'New session',\n    data: {\n      placement: 'main',",
     "    title: translateNow('common.newSession'),\n    data: {\n      placement: 'main',"),
    ("      label: 'Keyboard shortcuts',",
     "      label: translateNow('keybinds.actions.keybinds.openPanel'),"),
    ("    title: stored ? storedSessionTitle(stored) : 'New session',",
     "    title: stored ? storedSessionTitle(stored) : translateNow('common.newSession'),"),
    ("    label: 'Toggle logs',", "    label: translateNow('common.moreActions'),"),
])

# index.tsx — ChatHeader
apply(BASE + 'app/chat/index.tsx', [
    ("  const title = activeStoredSession ? sessionTitle(activeStoredSession) : 'New session'",
     "  const title = activeStoredSession ? sessionTitle(activeStoredSession) : translateNow('common.newSession')"),
])

# quick-entry-app.tsx
apply(BASE + 'app/quick-entry/quick-entry-app.tsx', [
    ("export function QuickEntryApp() {", "export function QuickEntryApp() {\n  const { t } = useI18n()"),
    ('aria-label="Quick Entry"', 'aria-label={t.settings.quickEntry.windowAriaLabel}'),
    ("<option value={QUICK_TARGET_CURRENT}>Current chat</option>",
     "<option value={QUICK_TARGET_CURRENT}>{t.settings.quickEntry.currentTarget}</option>"),
    ("<option value={QUICK_TARGET_NEW}>New session</option>",
     "<option value={QUICK_TARGET_NEW}>{t.settings.quickEntry.newTarget}</option>"),
])

# generate-unavailable.tsx
apply(BASE + 'app/pet-generate/components/generate-unavailable.tsx', [
    ("export function GenerateUnavailable({ onSetup }: GenerateUnavailableProps) {",
     "export function GenerateUnavailable({ onSetup }: GenerateUnavailableProps) {\n  const { t } = useI18n()"),
    ("        <span>Grab a key from</span>",
     "        <span>{t.commandCenter.generatePet.grabKeyFrom}</span>"),
])

# reference-chip.tsx — useI18n УЖЕ есть (строка 5/17), только замена
apply(BASE + 'app/pet-generate/components/reference-chip.tsx', [
    ('aria-label="Remove reference"', 'aria-label={t.commandCenter.generatePet.removeReference}'),
])

# pet-overlay-app.tsx
apply(BASE + 'app/pet-overlay/pet-overlay-app.tsx', [
    ("export function PetOverlayApp() {", "export function PetOverlayApp() {\n  const { t } = useI18n()"),
    ('aria-label="Open in Hermes"', 'aria-label={t.pet.openInHermes}'),
    ('title="Open in Hermes"', 'title={t.pet.openInHermes}'),
])
