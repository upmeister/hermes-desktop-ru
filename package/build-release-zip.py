#!/usr/bin/env python3
"""Build the public release zip from package/ + root docs.

Layout inside the zip (flat root, Windows-friendly):
  install.bat / install.ps1 / install-asar.ps1
  *.mjs, registry.json, overrides.json, EXPECTED_COMMIT
  files/ru.ts, files/ru-constants.ts, files/ru-locales.ts
  README.md, LICENSE, CHANGELOG.md   (if present next to package/)

Usage:
  python3 package/build-release-zip.py [out.zip]
"""
from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

CORE = [
    "install.bat",
    "install.ps1",
    "install-asar.ps1",
    "apply-hardcodes.mjs",
    "deps-health.mjs",
    "structural-i18n.mjs",
    "probe-ru.mjs",
    "gen-registry.mjs",  # optional for end users, useful for contributors
    "registry.json",
    "overrides.json",
    "EXPECTED_COMMIT",
]
FILES = [
    "files/ru.ts",
    "files/ru-constants.ts",
    "files/ru-locales.ts",
]
ROOT_DOCS = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
]


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist" / "hermes-desktop-ru-v7.6.1.zip"
    out.parent.mkdir(parents=True, exist_ok=True)

    missing = []
    for rel in CORE + FILES:
        if not (HERE / rel).exists():
            missing.append(f"package/{rel}")
    if missing:
        print("MISSING:", *missing, sep="\n  ")
        return 1

    # Guard: locale sync
    ru_src = ROOT / "i18n" / "ru.ts"
    ru_pkg = HERE / "files" / "ru.ts"
    if ru_src.exists() and ru_src.read_bytes() != ru_pkg.read_bytes():
        print("WARN: i18n/ru.ts != package/files/ru.ts — sync before release")

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in CORE:
            zf.write(HERE / rel, arcname=rel)
        for rel in FILES:
            zf.write(HERE / rel, arcname=rel)
        for rel in ROOT_DOCS:
            p = ROOT / rel
            if p.exists():
                zf.write(p, arcname=rel)

    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    names = sorted(zipfile.ZipFile(out).namelist())
    print(f"OK {out}  ({out.stat().st_size} bytes)")
    print(f"sha256 {digest}")
    print(f"files ({len(names)}):")
    for n in names:
        print(f"  {n}")
    # hard checks
    assert "probe-ru.mjs" in names
    assert "files/ru.ts" in names
    assert "install.bat" in names
    assert not any(n == "ru.ts" for n in names), "locales must live under files/"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
