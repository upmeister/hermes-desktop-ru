#!/usr/bin/env python3
"""Build the public release zips from package/ + root docs.

Layout inside the zips (flat root, cross-platform):
  hermes-desktop-ru-plugins-v<ver>.zip:
    install.bat / install.ps1 / install-asar.ps1 / install.sh / install.mjs
    *.mjs, registry.json, overrides.json, EXPECTED_COMMIT
    files/ru-locales.ts, files/ru-bots-locales.ts
    README.md, LICENSE, CHANGELOG.md
  hermes-desktop-ru-intro-v<ver>.zip:
    install.bat / install.ps1 / install-asar.ps1 / install.sh / install.mjs
    *.mjs, registry.json, overrides.json, EXPECTED_COMMIT
    files/intro-ru.ts
    README.md, LICENSE, CHANGELOG.md

Usage:
  python3 package/build-release-zip.py [outdir]

Produces two zips in outdir (default: dist/).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

CORE = [
    "install.bat",
    "install.ps1",
    "install-asar.ps1",
    "install.sh",
    "install.mjs",
    "apply-hardcodes.mjs",
    "measure-locales.mjs",
    "deps-health.mjs",
    "structural-i18n.mjs",
    "probe-ru.mjs",
    "gen-registry.mjs",
    "registry.json",
    "overrides.json",
    "EXPECTED_COMMIT",
]

PLUGIN_FILES = [
    "files/ru-locales.ts",      # kanban plugin locale
    "files/ru-bots-locales.ts", # bots plugin locale
]

INTRO_FILES = [
    "files/intro-ru.ts",        # greetings (intro) locale
]

ROOT_DOCS = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
]


def run_tsc_gate(tsc: Path, files: list[Path]) -> bool:
    """Run tsc --noCheck on given files. Returns True if all pass."""
    for p in files:
        if not p.exists():
            continue
        r = subprocess.run(
            [str(tsc), "--noCheck", "--noEmit", "--skipLibCheck", "--target", "es2022",
             "--module", "esnext", "--moduleResolution", "bundler", str(p)],
            capture_output=True, text=True)
        if r.returncode != 0:
            print(f"TS-SYNTAX FAIL: {p.name}")
            print(r.stdout[-2000:] or r.stderr[-2000:])
            return False
    return True


def build_zip(name: str, core_files: list[str], extra_files: list[str], out: Path, ver: str) -> int:
    """Build a single zip. Returns 0 on success, 1 on failure."""
    zip_path = out / f"hermes-desktop-ru-{name}-v{ver}.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    missing = []
    for rel in core_files + extra_files:
        if not (HERE / rel).exists():
            missing.append(f"package/{rel}")
    if missing:
        print(f"MISSING for {name}:", *missing, sep="\n  ")
        return 1

    # TS syntax gate for .ts files in extra_files
    tsc_candidates = [
        ROOT / "node_modules" / ".bin" / "tsc",
        HERE / "node_modules" / ".bin" / "tsc",
        Path.home() / "projects" / "hermes-agent-dev" / "node_modules" / ".bin" / "tsc",
    ]
    tsc = next((p for p in tsc_candidates if p.exists()), None)
    if tsc is not None:
        ts_files = [HERE / rel for rel in extra_files if rel.endswith(".ts")]
        if not run_tsc_gate(tsc, ts_files):
            return 1
        print(f"tsc-gate: {name} files/*.ts OK")

    # Guard: locale sync — hard fail
    ru_src = ROOT / "i18n" / "ru.ts"
    ru_pkg = HERE / "files" / "ru.ts"
    if ru_src.exists() and ru_src.read_bytes() != ru_pkg.read_bytes():
        print("ERROR: i18n/ru.ts != package/files/ru.ts — sync before release")
        return 1

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in core_files:
            zf.write(HERE / rel, arcname=rel)
        for rel in extra_files:
            zf.write(HERE / rel, arcname=rel)
        for rel in ROOT_DOCS:
            p = ROOT / rel
            if p.exists():
                zf.write(p, arcname=rel)

    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    names = sorted(zipfile.ZipFile(zip_path).namelist())
    print(f"OK {zip_path}  ({zip_path.stat().st_size} bytes)")
    print(f"sha256 {digest}")
    print(f"files ({len(names)}):")
    for n in names:
        print(f"  {n}")

    # Hard checks
    assert "probe-ru.mjs" in names
    assert "install.mjs" in names
    assert "install.sh" in names
    assert "install.bat" in names
    assert not any(n == "ru.ts" for n in names), "locales must live under files/"
    return 0


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"

    # Read version from package.json
    import json
    ver = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]

    print(f"=== Building hermes-desktop-ru {ver} ===")
    print()

    # Build plugins zip
    print("--- plugins ---")
    if build_zip("plugins", CORE, PLUGIN_FILES, out, ver):
        return 1
    print()

    # Build intro zip
    print("--- intro ---")
    if build_zip("intro", CORE, INTRO_FILES, out, ver):
        return 1
    print()

    print("=== Both zips built successfully ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())