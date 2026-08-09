#!/usr/bin/env python3
"""Поиск битых значений в ru.ts (пустые / оборванные функции) + en-значения для них."""
import re, json

KEY_RE = re.compile(r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))\s*:\s*(?P<rest>.*?)$")

def parse(path, wrapper):
    src = open(path, encoding='utf-8').read()
    i = src.find(wrapper)
    lines = src[i + len(wrapper):].splitlines()
    stack = []
    blocks = []
    current = None
    for line in lines:
        km = KEY_RE.match(line)
        indent = len(re.match(r'^(\s*)', line).group(1))
        if km:
            key = km.group('word') or km.group('sq') or km.group('dq') or km.group('num')
            while stack and stack[-1][0] >= indent:
                stack.pop()
            stack.append((indent, key))
            path = '.'.join(s[1] for s in stack)
            rest = km.group('rest')
            blocks.append({'indent': indent, 'path': path, 'key_token': km.group(0).split(':')[0].strip(),
                           'rest': rest, 'lines': [line]})
            current = len(blocks) - 1
        else:
            if current is not None:
                blocks[current]['lines'].append(line)
    return blocks

def full_value(block):
    """Полное значение блока: всё после ':' первой строки, включая продолжения."""
    first = block['lines'][0]
    colon = first.find(':')
    val = first[colon + 1:].strip()
    cont = [l.strip() for l in block['lines'][1:]]
    if cont:
        val = val + '\n' + '\n'.join(cont)
    return val

ru_blocks = parse('/home/covhnw/projects/hermes-desktop-ru/i18n/ru.ts', 'defineLocale({')
en_blocks = parse('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts', 'export const en: Translations = {')
en_map = {b['path']: b for b in en_blocks}

broken = []
for b in ru_blocks:
    v = full_value(b).rstrip(',')
    # пустое значение или функция без тела (заканчивается на '=>')
    if v == '' or v.endswith('=>') or v == ',' :
        broken.append(b['path'])
    elif re.search(r'\)\s*=>\s*,?$', v) and '`' not in v:
        broken.append(b['path'])

print(f'битых значений: {len(broken)}')
out = {}
for p in sorted(set(broken)):
    eb = en_map.get(p)
    ev = full_value(eb) if eb else '<нет в en>'
    out[p] = ev
    print(f'\n{p}\n  ru: {full_value(next(b for b in ru_blocks if b["path"]==p))[:80]}\n  en: {ev[:200]}')
json.dump(out, open('/home/covhnw/projects/hermes-desktop-ru/broken_keys.json', 'w'), ensure_ascii=False, indent=1)
