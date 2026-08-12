#!/usr/bin/env python3
"""Проверка: все t.<path> из файлов → наличие и непустое значение в ru.ts."""
import re, json

BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/'
files = [
    'app/settings/providers-settings.tsx',
    'app/settings/custom-endpoints-settings.tsx',
    'app/settings/keys-settings.tsx',
    'app/settings/plugins-settings.tsx',
]
ru = open(BASE + 'i18n/ru.ts', encoding='utf-8').read()
en = open(BASE + 'i18n/en.ts', encoding='utf-8').read()

# собрать t.xxx.yyy пути (t.settings..., t.common..., t.commandCenter...)
paths = set()
for f in files:
    src = open(BASE + f, encoding='utf-8').read()
    for m in re.finditer(r'\bt\.([a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z][a-zA-Z0-9]*)+)', src):
        paths.add(m.group(1))

def lookup(text, path):
    """Достать значение по dot-пути из TS-объекта (грубая эвристика по блокам)."""
    cur = text
    for part in path.split('.'):
        # найти 'part:' на текущем уровне
        m = re.search(r'(?m)^\s*' + re.escape(part) + r':\s*', cur)
        if not m:
            return None
        cur = cur[m.end():]
        # если значение начинается с '{' — взять сбалансированный блок
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
            # скаляр: до запятой на том же уровне (не в скобках)
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

problems = []
for p in sorted(paths):
    ru_v = lookup(ru, p)
    en_v = lookup(en, p)
    if ru_v is None:
        problems.append(f'MISSING_IN_RU: {p}')
    elif ru_v in ("''", '', '`', '<func>') and en_v not in ("''", '', '`'):
        problems.append(f'EMPTY_IN_RU: {p} = {ru_v[:60]!r}')
    elif ru_v.startswith('{') and not en_v.startswith('{'):
        problems.append(f'TYPE_MISMATCH(obj in ru, scalar in en): {p}')

print(f'всего t-путей: {len(paths)}')
if problems:
    print('ПРОБЛЕМЫ:')
    for x in problems:
        print(' ', x)
else:
    print('проблем нет')
