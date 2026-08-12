#!/usr/bin/env python3
"""Полная проверка: все t.* пути всех компонентов src → наличие/пустота в ru.ts."""
import re, os

BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/'
ru = open(BASE + 'i18n/ru.ts', encoding='utf-8').read()
en = open(BASE + 'i18n/en.ts', encoding='utf-8').read()

paths = set()
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.vite', 'dist')]
    for f in files:
        if not (f.endswith('.tsx') or f.endswith('.ts')) or f.endswith('.test.tsx') or f.endswith('.test.ts') or f.endswith('.d.ts'):
            continue
        if 'i18n/' in root or 'test' in root.lower():
            continue
        src = open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'\bt\.([a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z][a-zA-Z0-9]*)+)', src):
            paths.add((m.group(1), os.path.join(root, f).replace(BASE, '')))

def lookup(text, path):
    cur = text
    for part in path.split('.'):
        m = re.search(r'(?m)^\s*' + re.escape(part) + r':\s*', cur)
        if not m:
            return None
        cur = cur[m.end():]
        if cur.lstrip().startswith('{'):
            depth, i = 0, 0
            s = cur.lstrip()
            while i < len(s):
                if s[i] == '{': depth += 1
                elif s[i] == '}':
                    depth -= 1
                    if depth == 0: break
                i += 1
            cur = s[:i+1]
        else:
            i, depth = 0, 0
            s = cur
            while i < len(s):
                c = s[i]
                if c in '({[': depth += 1
                elif c in ')}]': depth -= 1
                elif c == ',' and depth == 0: break
                elif c == '\n' and depth == 0: break
                i += 1
            cur = s[:i]
        if cur.lstrip().startswith('path =>') or cur.lstrip().startswith('('):
            return '<func>'
    return cur.strip()

missing, empty = [], []
for p, f in sorted(paths):
    ru_v = lookup(ru, p)
    if ru_v is None:
        missing.append((p, f))
    elif ru_v in ("''", '', '`'):
        empty.append((p, f))

print(f'всего t-путей: {len(paths)}')
print(f'MISSING: {len(missing)}')
for p, f in missing:
    print(f'  {p}  ← {f}')
print(f'EMPTY: {len(empty)}')
for p, f in empty:
    print(f'  {p}  ← {f}')
