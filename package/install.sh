#!/usr/bin/env bash
# Hermes Desktop RU installer wrapper (Linux / macOS).
# Experimental — the author has not run this on a live Mac/Linux Desktop.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: Node.js 18+ is required (node not in PATH)" >&2
  exit 1
fi
exec node "$DIR/install.mjs" "$@"