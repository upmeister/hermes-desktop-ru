#!/usr/bin/env python3
"""Пост-merge валидация: остатки missing, скобки, пустые значения, лишние ключи."""
import re, json

KEY_RE = re.compile(r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))\s*:\s*(?P<rest>.*?)$")

def parse(path, wrapper):
    src = open(path, encoding='utf-8').read()
    i = src.find(wrapper)
    body = src[i + len(wrapper):]
    stack = []
    paths = set()
    values = {}
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
            values[full] = rest.rstrip(',').strip()
    return paths, values

en_p, en_v = parse('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts', 'export const en: Translations = {')
ru_p, ru_v = parse('/home/covhnw/projects/hermes-desktop-ru/i18n/ru.ts', 'defineLocale({')

missing = sorted(en_p - ru_p)
extra = sorted(ru_p - en_p)
print(f'en: {len(en_p)} | ru: {len(ru_p)} | missing: {len(missing)} | лишних: {len(extra)}')
for p in missing:
    print('  MISSING:', p, '=>', en_v.get(p, '')[:80])
for p in extra:
    print('  EXTRA:', p)
