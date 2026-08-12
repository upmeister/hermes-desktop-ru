#!/usr/bin/env python3
"""Точный diff ключей en.ts vs ru.ts: поиск по отступам (2*level)."""
import re

def find_sec(text, path):
    """Вернуть (found, value-raw) для dot-пути, следуя отступам 2*level."""
    level = 1  # внутри export const ... = {
    cur = text
    for part in path.split('.'):
        indent = '  ' * level
        m = re.search(r'(?m)^' + indent + re.escape(part) + r':\s*', cur)
        if not m:
            return False, None
        cur = cur[m.end():]
        if cur.lstrip().startswith('{'):
            level += 1
            d, i = 0, 0
            s = cur.lstrip()
            while i < len(s):
                if s[i] == '{': d += 1
                elif s[i] == '}':
                    d -= 1
                    if d == 0: break
                i += 1
            cur = s[:i+1]
        else:
            # скаляр/функция: до запятой на уровне 0
            i, d = 0, 0
            while i < len(cur):
                c = cur[i]
                if c in '({[': d += 1
                elif c in ')}]':
                    if d == 0: break
                    d -= 1
                elif c == ',' and d == 0: break
                elif c == '\n' and d == 0: break
                i += 1
            cur = cur[:i]
            if cur.lstrip().startswith('path =>') or cur.lstrip().startswith('('):
                return True, '<func>'
            return True, cur.strip()
    return True, cur.strip()

def all_keys(text):
    """Все dot-пути листьев (рекурсивно по отступам)."""
    out = {}
    def walk(t, prefix, level):
        indent = '  ' * level
        # найти все ключи на этом уровне
        for m in re.finditer(r'(?m)^' + indent + r'([A-Za-z_][A-Za-z0-9_]*):\s*', t):
            key = m.group(1)
            rest = t[m.end():]
            if rest.lstrip().startswith('{'):
                d, i = 0, 0
                s = rest.lstrip()
                while i < len(s):
                    if s[i] == '{': d += 1
                    elif s[i] == '}':
                        d -= 1
                        if d == 0: break
                    i += 1
                out[prefix + key] = '<obj>'
                walk(s[:i], prefix + key + '.', level + 1)
            else:
                i, d = 0, 0
                while i < len(rest):
                    c = rest[i]
                    if c in '({[': d += 1
                    elif c in ')}]':
                        if d == 0: break
                        d -= 1
                    elif c == ',' and d == 0: break
                    elif c == '\n' and d == 0: break
                    i += 1
                out[prefix + key] = rest[:i].strip()
        # найти не-ASCII ключи (в кавычках, типа 'session.new')
        for m in re.finditer(r"(?m)^" + indent + r"'([^']+)':\s*", t):
            out[prefix + m.group(1)] = '<q>'
    # старт: тело export const ... = {  /  defineLocale({
    if 'defineLocale({' in text:
        start = text.index('defineLocale({') + 13
    else:
        start = text.index('= {') + 2
    d, i = 0, start
    while i < len(text):
        c = text[i]
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: break
        i += 1
    walk(text[start+1:i], '', 1)
    return out

en = all_keys(open('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts', encoding='utf-8').read())
ru = all_keys(open('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/ru.ts', encoding='utf-8').read())
print(f'en: {len(en)}  ru: {len(ru)}')
missing = sorted(k for k in en if k not in ru)
extra = sorted(k for k in ru if k not in en)
print(f'MISSING в ru: {len(missing)}')
for k in missing: print(f'  {k}')
print(f'ЛИШНИЕ в ru: {len(extra)}')
for k in extra: print(f'  {k}')
