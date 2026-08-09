#!/usr/bin/env python3
"""Карта добавленных warment-ключей: полные пути + значения en + переводы ru."""
import json, re

KEY_RE = re.compile(r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))\s*:\s*(?P<rest>.*?)$")

def parse(path, wrapper):
    """Возвращает (paths:set, values:dict[path, raw_value])."""
    src = open(path, encoding='utf-8').read()
    i = src.find(wrapper)
    body = src[i + len(wrapper):]
    stack = []          # (indent, key)
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

en_w, val_w = parse('/home/covhnw/projects/warment-ru/patches/i18n/en.ts', 'export const en: Translations = {')
en_s, val_s = parse('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts', 'export const en: Translations = {')
ru_w, val_ru = parse('/home/covhnw/projects/warment-ru/patches/i18n/ru.ts', 'defineLocale({')

added = sorted(en_w - en_s)
print(f'warment добавил путей: {len(added)}')
print(f'из них переведено в его ru.ts: {sum(1 for p in added if p in ru_w)}')
print(f'из них НЕ переведено в его ru.ts: {sum(1 for p in added if p not in ru_w)}')

out = {}
for p in added:
    out[p] = {
        'en': val_w.get(p, ''),
        'ru': val_ru.get(p, ''),
        'translated': p in ru_w,
    }
json.dump(out, open('/home/covhnw/projects/hermes-desktop-ru/warment_added_keys.json', 'w'),
          ensure_ascii=False, indent=1)
print('сохранено: warment_added_keys.json')
print()
print('=== примеры ===')
for p in added[:25]:
    o = out[p]
    print(f'  {p}')
    print(f'    en: {o["en"][:90]}')
    print(f'    ru: {o["ru"][:90]}')
