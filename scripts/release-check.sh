#!/usr/bin/env bash
# release-check.sh — проверки перед релизом hermes-desktop-ru.
# Ловит «забытые строчки»: старую версию/doctor-N в README и коде, разъехавшуюся
# версию, устаревший EXPECTED_COMMIT, test-zip в dist, сломанный синтаксис.
#
# Использование: scripts/release-check.sh <пред.версия> [пред.doctor-N] [--no-pc]
#   ./scripts/release-check.sh 1.1.1 859        # сверить с ПК (EXPECTED_COMMIT)
#   ./scripts/release-check.sh 1.1.1 859 --no-pc # без ssh к covhnw-pc2
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1
PREV_VER="${1:-}"
PREV_DOCTOR="${2:-}"
FAIL=0

say()  { printf '\033[1;32m✓ %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m⚠ %s\033[0m\n' "$*"; }
err()  { printf '\033[1;31m✗ %s\033[0m\n' "$*"; FAIL=1; }

echo "== release-check для $(git log --oneline -1 2>/dev/null || echo '?') =="

# 1. Версия согласована в трёх местах
VER="$(python3 -c "import json;print(json.load(open('package.json'))['version'])" 2>/dev/null)"
FB="$(grep -oP "FALLBACK_VERSION = '\K[^']+" package/install.mjs 2>/dev/null)"
ZIPLINE="$(grep -oP 'hermes-desktop-ru-v\K[0-9.]+(?=\.zip)' package/build-release-zip.py 2>/dev/null)"
if [ -n "$VER" ] && [ "$VER" = "$FB" ] && [ "$VER" = "$ZIPLINE" ]; then
  say "версия согласована (package.json=install.mjs=zip: $VER)"
else
  err "версия разъехалась: package.json=$VER install.mjs=$FB zip=$ZIPLINE"
fi

# 2. Новые числа присутствуют в README
grep -q "v$VER" README.md 2>/dev/null || err "в README.md нет шапки с v$VER"
grep -q "v$VER" README.en.md 2>/dev/null || err "в README.en.md нет шапки с v$VER"

# 3. Sweep старых чисел (живые файлы; CHANGELOG/UPSTREAM-WATCH — история, не трогаем)
SCAN_FILES="README.md README.en.md package.json package/install.mjs package/apply-hardcodes.mjs package/gen-registry.mjs package/structural-i18n.mjs package/deps-health.mjs package/probe-ru.mjs package/build-release-zip.py bin/hermes-desktop-ru.mjs"
if [ -n "$PREV_VER" ]; then
  HITS="$(grep -Hn --fixed-strings "$PREV_VER" $SCAN_FILES 2>/dev/null || true)"
  if [ -n "$HITS" ]; then warn "найден старый PREV_VER ($PREV_VER):"; printf '%s\n' "$HITS"; fi
fi
if [ -n "$PREV_DOCTOR" ]; then
  HITS="$(grep -HnE "doctor $PREV_DOCTOR|$PREV_DOCTOR/$PREV_DOCTOR|$PREV_DOCTOR правил|$PREV_DOCTOR-rule" $SCAN_FILES 2>/dev/null || true)"
  if [ -n "$HITS" ]; then warn "найден старый doctor ($PREV_DOCTOR):"; printf '%s\n' "$HITS"; fi
fi

# 4. EXPECTED_COMMIT == HEAD ПК (если ПК доступен)
if [[ " $* " != *" --no-pc "* ]]; then
  PC_HEAD="$(ssh covhnw-pc2 "cd C:/Users/covhnw/AppData/Local/hermes/hermes-agent && git rev-parse HEAD" 2>/dev/null | tr -d '\r\n')"
  EXP="$(tr -d '\r\n' < package/EXPECTED_COMMIT 2>/dev/null)"
  if [ -n "$PC_HEAD" ] && [ -n "$EXP" ] && [ "$PC_HEAD" = "$EXP" ]; then
    say "EXPECTED_COMMIT = HEAD ПК (${EXP:0:12})"
  elif [ -z "$PC_HEAD" ]; then
    warn "ПК недоступен — EXPECTED_COMMIT не сверен"
  else
    err "EXPECTED_COMMIT (${EXP:0:12}) != HEAD ПК (${PC_HEAD:0:12}) — переснять!"
  fi
fi

# 5. В dist нет test-артефактов
if ls dist/*-test-* 2>/dev/null | grep -q .; then
  warn "в dist есть test-артефакты (не путать с релизным ассетом):"
  ls dist/*-test-* 2>/dev/null
fi

# 6. Синтаксис ключевых mjs
for f in bin/hermes-desktop-ru.mjs package/install.mjs package/apply-hardcodes.mjs; do
  if node --check "$f" >/dev/null 2>&1; then say "node --check $f"; else err "node --check $f (сломан!)"; fi
done

echo
if [ "$FAIL" -eq 0 ]; then
  echo "✅ release-check: всё чисто — можно релизить"
else
  echo "❌ release-check: есть проблемы — см. выше"
fi
exit "$FAIL"