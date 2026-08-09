#!/usr/bin/env python3
"""Сборка translation table для merge: warment-переводы missing + список непокрытых."""
import json, re

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

EN = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts'
RU_OURS = '/home/covhnw/projects/hermes-desktop-ru/i18n/ru.ts'
RU_WAR = '/home/covhnw/projects/warment-ru/patches/i18n/ru.ts'
OUT_DIR = '/home/covhnw/projects/hermes-desktop-ru/'

en_s, en_vals = parse(EN, 'export const en: Translations = {')
ru_o, _ = parse(RU_OURS, 'defineLocale({')
ru_w, ru_w_vals = parse(RU_WAR, 'defineLocale({')

missing = sorted(en_s - ru_o)
print(f'missing: {len(missing)}')

T = {}
for p in missing:
    if p in ru_w:
        T[p] = ru_w_vals[p]
print(f'из warment: {len(T)}')

rest = [p for p in missing if p not in ru_w]
print(f'непокрыто: {len(rest)}')

# таблица непокрытых с en-значениями для ручного перевода
manual = {p: en_vals.get(p, '') for p in rest}
json.dump(manual, open(OUT_DIR + 'manual_todo.json', 'w'), ensure_ascii=False, indent=1)

# warment-переводы → отдельная таблица (мержится поверх старой)
json.dump(T, open(OUT_DIR + 'warment_translations.json', 'w'), ensure_ascii=False, indent=1)

print('\n=== 102 непокрытых (key => en) ===')
for p in rest:
    print(f'{p} => {en_vals.get(p, "")[:100]}')
