#!/usr/bin/env python3
"""Сравнение ключей en.ts (worktree) vs ru.ts мода + покрытие источниками."""
import re, json, sys

KEY_RE = re.compile(r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))\s*:\s*(?P<rest>.*?)$")

def paths_of(path, wrapper):
    src = open(path, encoding='utf-8').read()
    i = src.find(wrapper)
    body = src[i + len(wrapper):]
    stack = []
    paths = set()
    for line in body.splitlines():
        m = KEY_RE.match(line)
        if not m:
            continue
        indent = len(m.group('indent'))
        key = m.group('word') or m.group('sq') or m.group('dq') or m.group('num')
        rest = m.group('rest').rstrip()
        is_container = rest.endswith('{')
        while stack and indent <= stack[-1][0]:
            stack.pop()
        full = '.'.join([s[1] for s in stack] + [key])
        stack.append((indent, key))
        if not is_container:
            paths.add(full)
    return paths

en = paths_of('apps/desktop/src/i18n/en.ts', 'export const en: Translations = {')
ru = paths_of('/home/covhnw/projects/hermes-desktop-ru/i18n/ru.ts', 'defineLocale({')
missing = sorted(en - ru)
extra = sorted(ru - en)
print(f'свежий en.ts: {len(en)} путей | ru.ts мода: {len(ru)} | missing: {len(missing)} | лишних: {len(extra)}')

table = json.load(open('/home/covhnw/projects/hermes-desktop-ru/translations_table.json'))
tkeys = set(table.keys())
cov_table = set(missing).intersection(tkeys)
print(f'таблица покрывает missing: {len(cov_table)}')

wr = paths_of('/home/covhnw/projects/warment-ru/patches/i18n/ru.ts', 'defineLocale({')
cov_war = set(missing).intersection(set(wr))
print(f'warment ru.ts: {len(wr)} путей, покрывает missing: {len(cov_war)}')
rest = set(missing) - tkeys - set(wr)
print(f'осталось непокрытым ничем: {len(rest)}')
if rest:
    print('примеры непокрытых:', list(sorted(rest))[:15])
