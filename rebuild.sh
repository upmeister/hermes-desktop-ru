#!/usr/bin/env bash
# Hermes Desktop — Russian i18n mod re-apply script
# Run this after `hermes update` to rebuild the Russian translation.
#
# Usage: bash ~/.hermes/desktop-ru-mod/rebuild.sh
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$(cygpath -u "$LOCALAPPDATA" 2>/dev/null || echo "$HOME/AppData/Local")/hermes}"
HERMES_SRC="$HERMES_HOME/hermes-agent"
DESKTOP_SRC="$HERMES_SRC/apps/desktop"
MOD_DIR="$HERMES_HOME/desktop-ru-mod"
DIST_BACKUP="$MOD_DIR/dist"

echo "=== Hermes Desktop Russian mod — rebuild ==="
echo "Source: $DESKTOP_SRC"
echo "Mod dir: $MOD_DIR"
echo ""

# --- 1. Check source exists ---
if [ ! -d "$DESKTOP_SRC/src/i18n" ]; then
  echo "ERROR: Desktop source not found at $DESKTOP_SRC"
  exit 1
fi

# --- 2. Restore mod files into source tree ---
echo "[1/6] Restoring i18n mod files..."
cp "$MOD_DIR/i18n/types.ts"    "$DESKTOP_SRC/src/i18n/types.ts"
cp "$MOD_DIR/i18n/languages.ts" "$DESKTOP_SRC/src/i18n/languages.ts"
cp "$MOD_DIR/i18n/catalog.ts"  "$DESKTOP_SRC/src/i18n/catalog.ts"
cp "$MOD_DIR/i18n/ru.ts"       "$DESKTOP_SRC/src/i18n/ru.ts"
cp "$MOD_DIR/i18n/ru-constants.ts" "$DESKTOP_SRC/src/app/settings/ru-constants.ts"
echo "  ✓ Mod files restored"

# --- 2b. Patch components and skills (replace hardcoded strings with t.* keys) ---
HERMES_SRC_NATIVE=$(cygpath -w "$HERMES_SRC" 2>/dev/null || echo "$HERMES_SRC")
MOD_DIR_NATIVE=$(cygpath -w "$MOD_DIR" 2>/dev/null || echo "$MOD_DIR")
VENV_PYTHON="$HERMES_SRC/venv/Scripts/python.exe"
echo "[2/6] Patching settings components..."
"$VENV_PYTHON" "$MOD_DIR_NATIVE/scripts/patch-components.py" "$HERMES_SRC_NATIVE" || echo "  [~] Component patching continued despite errors"
echo "[3/6] Patching skill descriptions..."
"$VENV_PYTHON" "$MOD_DIR_NATIVE/scripts/patch-skills.py" "$HERMES_SRC_NATIVE" || echo "  [~] Skill patching continued despite errors"

# --- 3. Rebuild frontend ---
echo "[4/6] Building desktop frontend..."
cd "$DESKTOP_SRC"
npm run build 2>&1 | tail -5
if [ ! -f "$DESKTOP_SRC/dist/index.html" ]; then
  echo "ERROR: Build failed — dist/index.html not found"
  exit 1
fi
echo "  ✓ Build complete"

# --- 4. Copy built dist to persistent location ---
echo "[5/6] Copying dist to $DIST_BACKUP..."
rm -rf "$DIST_BACKUP"
cp -r "$DESKTOP_SRC/dist" "$DIST_BACKUP"
echo "  ✓ Dist copied"

# --- 5. Patch resolveRendererIndex in electron-main.mjs ---
# Bug: Electron checks APP_ROOT/dist/index.html FIRST, which resolves to the
# English dist inside app.asar.unpacked/dist. Our HERMES_DESKTOP_WEB_DIST is
# checked SECOND and never used. Fix: put our override first.
echo "[6/6] Patching resolveRendererIndex to prefer HERMES_DESKTOP_WEB_DIST..."
for MJS in \
  "$DESKTOP_SRC/dist/electron-main.mjs" \
  "$HERMES_SRC/apps/desktop/release/win-unpacked/resources/app.asar.unpacked/dist/electron-main.mjs"; do
  if [ -f "$MJS" ]; then
    # Patch: swap candidate order so resolveWebDist() comes first
    sed -i 's|const candidates = \[path13\.join(APP_ROOT, "dist", "index\.html"), path13\.join(resolveWebDist(), "index\.html")\];|const candidates = [path13.join(resolveWebDist(), "index.html"), path13.join(APP_ROOT, "dist", "index.html")];|' "$MJS"
    echo "  ✓ Patched: $(basename "$MJS")"
  else
    echo "  [~] Skipped (not found): $(basename "$MJS")"
  fi
done

# --- 6b. Copy dist to app.asar.unpacked (fallback if env var not set) ---
ASAR_DIST="$HERMES_SRC/apps/desktop/release/win-unpacked/resources/app.asar.unpacked/dist"
if [ -d "$ASAR_DIST" ]; then
  echo "[6b] Copying dist to app.asar.unpacked..."
  rm -rf "$ASAR_DIST"
  cp -r "$DESKTOP_SRC/dist" "$ASAR_DIST"
  echo "  ✓ app.asar.unpacked/dist updated"
else
  echo "  [~] app.asar.unpacked/dist not found, skipping"
fi

# --- 7. Set env var (if not already set) ---
echo "Ensuring HERMES_DESKTOP_WEB_DIST is set..."
if [ -z "${HERMES_DESKTOP_WEB_DIST:-}" ]; then
  WIN_DIST=$(cygpath -w "$DIST_BACKUP" 2>/dev/null || echo "$DIST_BACKUP")
  setx HERMES_DESKTOP_WEB_DIST "$WIN_DIST" >/dev/null 2>&1
  echo "  ✓ Set HERMES_DESKTOP_WEB_DIST=$WIN_DIST (restart app to take effect)"
else
  echo "  ✓ Already set: $HERMES_DESKTOP_WEB_DIST"
fi

echo ""
echo "=== Done! Restart Hermes Desktop to apply Russian UI. ==="