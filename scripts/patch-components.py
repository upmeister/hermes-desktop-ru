#!/usr/bin/env python3
"""Patch Hermes Desktop component files to use translation keys."""
import sys
import os
import re

def patch_file(filepath, replacements):
    """Apply a list of (old, new) replacements to a file."""
    if not os.path.exists(filepath):
        print(f"  [!] File not found, skipping: {filepath}")
        return False

    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False


def add_useI18n_if_missing(filepath):
    """Add useI18n import and hook if not already present."""
    if not os.path.exists(filepath):
        print(f"  [!] File not found, skipping: {filepath}")
        return False

    with open(filepath, 'r') as f:
        content = f.read()

    if 'useI18n' in content:
        return False

    # Add import
    if "from '@/hermes'" in content:
        content = content.replace(
            "from '@/hermes'",
            "from '@/hermes'\nimport { useI18n } from '@/i18n'"
        )
    elif "from '@/components" in content:
        # Add after last import from @/
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') and '@/' in line:
                last_import_idx = i
        lines.insert(last_import_idx + 1, "import { useI18n } from '@/i18n'")
        content = '\n'.join(lines)

    # Find component function and add hook
    match = re.search(r'(export function \w+\([^)]*\)\s*\{)', content)
    if match:
        func_line = match.group(0)
        if 'const { t }' not in content:
            content = content.replace(
                func_line,
                func_line + '\n  const { t } = useI18n()'
            )

    with open(filepath, 'w') as f:
        f.write(content)
    return True


def patch_index(hermes_dir):
    """Patch settings/index.tsx - replace hardcoded nav labels."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/index.tsx')
    replacements = [
        ('label="Providers"', 'label={t.settings.nav.providers}'),
        ('label="Accounts"', 'label={t.settings.nav.accounts}'),
        ('label="API keys"', 'label={t.settings.nav.apiKeysSub}'),
        ('label="Tools"', 'label={t.settings.nav.tools}'),
        ('label="Settings"', 'label={t.settings.nav.settingsSub}'),
    ]
    if patch_file(filepath, replacements):
        print("  [✓] settings/index.tsx patched")
    else:
        print("  [~] settings/index.tsx already patched or not found")


def patch_config_settings(hermes_dir):
    """Patch config-settings.tsx."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/config-settings.tsx')
    add_useI18n_if_missing(filepath)
    patch_file(filepath, [
        ('LoadingState label="Loading Hermes configuration..."', 'LoadingState label={t.common.loadingConfig}'),
    ])
    print("  [✓] config-settings.tsx patched")


def patch_keys_settings(hermes_dir):
    """Patch keys-settings.tsx."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/keys-settings.tsx')
    add_useI18n_if_missing(filepath)
    patch_file(filepath, [
        ('LoadingState label="Loading API keys and credentials..."', 'LoadingState label={t.common.loadingKeys}'),
    ])
    print("  [✓] keys-settings.tsx patched")


def patch_model_settings(hermes_dir):
    """Patch model-settings.tsx."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/model-settings.tsx')
    add_useI18n_if_missing(filepath)
    patch_file(filepath, [
        ('LoadingState label="Loading model configuration..."', 'LoadingState label={t.common.loadingModel}'),
    ])
    print("  [✓] model-settings.tsx patched")


def patch_gateway_settings(hermes_dir):
    """Patch gateway-settings.tsx - the biggest one with ~35 strings."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/gateway-settings.tsx')
    add_useI18n_if_missing(filepath)
    replacements = [
        ('title="Gateway Connection"', 'title={t.gatewayPage.gatewayConnection}'),
        ('<Pill tone="primary">env override</Pill>', '<Pill tone="primary">{t.gatewayPage.envOverride}</Pill>'),
        ('title="Local gateway"', 'title={t.gatewayPage.localGateway}'),
        ('description="Start a private Hermes backend on localhost. This is the default and works offline."', 'description={t.gatewayPage.localGatewayDesc}'),
        ('title="Remote gateway"', 'title={t.gatewayPage.remoteGateway}'),
        ('description="Connect this desktop shell to a remote Hermes backend. Hosted gateways use OAuth or a username and password; self-hosted ones may use a session token."', 'description={t.gatewayPage.remoteGatewayDesc}'),
        ('title="Remote URL"', 'title={t.gatewayPage.remoteUrl}'),
        ('description="Base URL for the remote dashboard backend. Path prefixes are supported, for example /hermes."', 'description={t.gatewayPage.remoteUrlDesc}'),
        ('placeholder="https://gateway.example.com/hermes"', 'placeholder={t.gatewayPage.remoteUrlPlaceholder}'),
        ('title="Authentication"', 'title={t.gatewayPage.authentication}'),
        ('title="Session token"', 'title={t.gatewayPage.sessionToken}'),
        ('description="The dashboard session token used for REST and WebSocket access. Leave blank to keep the saved token."', 'description={t.gatewayPage.sessionTokenDesc}'),
        ('title="Diagnostics"', 'title={t.gatewayPage.diagnostics}'),
        ('description="Reveal desktop.log in your file manager — useful when the gateway fails to start."', 'description={t.gatewayPage.diagnosticsDesc}'),
        ('<span>Test remote</span>', '<span>{t.gatewayPage.testRemote}</span>'),
        ('<span>Save for next restart</span>', '<span>{t.gatewayPage.saveForNextRestart}</span>'),
        ('Save and reconnect', '{t.gatewayPage.saveAndReconnect}'),
        ('Open logs', '{t.gatewayPage.openLogs}'),
        ('Checking how this gateway authenticates...', 't.gatewayPage.checkingAuth'),
        ('title="Gateway settings unavailable"', 'title={t.gatewayPage.settingsUnavailable}'),
        ('description="The desktop IPC bridge does not expose gateway settings."', 'description={t.gatewayPage.settingsUnavailableDesc}'),
    ]
    if patch_file(filepath, replacements):
        print("  [✓] gateway-settings.tsx patched")
    else:
        print("  [~] gateway-settings.tsx already patched or not found")


def patch_mcp_settings(hermes_dir):
    """Patch mcp-settings.tsx (may not exist in newer versions)."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/mcp-settings.tsx')
    if not os.path.exists(filepath):
        print("  [~] mcp-settings.tsx not found (version may have renamed/removed it)")
        return
    add_useI18n_if_missing(filepath)
    replacements = [
        ('title="No MCP servers"', 'title={t.mcpPage.noServers}'),
        ('description="Add a stdio or HTTP server to expose MCP tools."', 'description={t.mcpPage.noServersDesc}'),
        ("'New server'", "t.mcpPage.newServer"),
        ("'Reload MCP'", "t.mcpPage.reloadMcp"),
        ("'Reloading...'", "t.mcpPage.reloading"),
        ("'Remove'", "t.mcpPage.remove"),
        ("'Save server'", "t.mcpPage.saveServer"),
        ("'Saving...'", "t.mcpPage.saving"),
        ("<span>Name</span>", "<span>{t.mcpPage.name}</span>"),
        ("<span>Server JSON</span>", "<span>{t.mcpPage.serverJson}</span>"),
    ]
    if patch_file(filepath, replacements):
        print("  [✓] mcp-settings.tsx patched")
    else:
        print("  [~] mcp-settings.tsx already patched or not found")


def patch_sessions_settings(hermes_dir):
    """Patch sessions-settings.tsx (may not exist in newer versions)."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/sessions-settings.tsx')
    if not os.path.exists(filepath):
        print("  [~] sessions-settings.tsx not found (version may have renamed/removed it)")
        return
    add_useI18n_if_missing(filepath)
    replacements = [
        ('title="Archived sessions"', 'title={t.sessionsPage.archivedSessions}'),
        ('title="Nothing archived"', 'title={t.sessionsPage.nothingArchived}'),
        ('description="Archive a chat to hide it here."', 'description={t.sessionsPage.archiveHint}'),
        ('<span>Unarchive</span>', '<span>{t.sessionsPage.unarchive}</span>'),
        ('title="Default project directory"', 'title={t.sessionsPage.defaultProjectDir}'),
        ("'Not set'", "t.sessionsPage.notSet"),
        ("'Change' : 'Choose'", "t.sessionsPage.change : t.sessionsPage.choose"),
    ]
    if patch_file(filepath, replacements):
        print("  [✓] sessions-settings.tsx patched")
    else:
        print("  [~] sessions-settings.tsx already patched or not found")


def patch_providers_settings(hermes_dir):
    """Patch providers-settings.tsx."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/providers-settings.tsx')
    add_useI18n_if_missing(filepath)
    patch_file(filepath, [
        ('LoadingState label="Loading providers..."', 'LoadingState label={t.common.loadingProviders}'),
    ])
    print("  [✓] providers-settings.tsx patched")


def patch_toolset_config(hermes_dir):
    """Patch toolset-config-panel.tsx."""
    filepath = os.path.join(hermes_dir, 'apps/desktop/src/app/settings/toolset-config-panel.tsx')
    add_useI18n_if_missing(filepath)
    patch_file(filepath, [
        ('PageLoader className="min-h-32" label="Loading configuration"', 'PageLoader className="min-h-32" label={t.common.loadingConfig}'),
    ])
    print("  [✓] toolset-config-panel.tsx patched")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: patch-components.py <hermes-dir>")
        sys.exit(1)

    hermes_dir = sys.argv[1]
    print("Patching components...")

    patch_index(hermes_dir)
    patch_config_settings(hermes_dir)
    patch_keys_settings(hermes_dir)
    patch_model_settings(hermes_dir)
    patch_gateway_settings(hermes_dir)
    patch_mcp_settings(hermes_dir)
    patch_sessions_settings(hermes_dir)
    patch_providers_settings(hermes_dir)
    patch_toolset_config(hermes_dir)

    print("Done patching components")