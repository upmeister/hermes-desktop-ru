#!/usr/bin/env bash
# Hermes Desktop RU installer wrapper (Linux / macOS).
# Linux: author-tested. macOS: experimental (no live Desktop run).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"

find_node() {
  if command -v node >/dev/null 2>&1; then
    command -v node
    return 0
  fi
  local home="${HERMES_HOME:-${HOME}/.hermes}"
  local c
  for c in "${home}/node/bin/node" "${HOME}/.hermes/node/bin/node"; do
    if [ -x "$c" ]; then
      printf '%s\n' "$c"
      return 0
    fi
  done
  return 1
}

NODE_BIN="$(find_node || true)"
if [ -z "${NODE_BIN}" ]; then
  echo "ERROR: Node.js 18+ is required (node not in PATH)." >&2
  echo "If Desktop was already packed, its managed Node is often at" >&2
  echo "  \$HERMES_HOME/node/bin/node  or  ~/.hermes/node/bin/node" >&2
  echo "Add that to PATH, or install Node 18+." >&2
  exit 1
fi
exec "$NODE_BIN" "$DIR/install.mjs" "$@"
