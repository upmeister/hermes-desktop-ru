#!/usr/bin/env python3
"""Точный diff ключей en.ts vs ru.ts (рекурсивный парсер объектов)."""
import re

def parse_keys(text):
    """Все dot-пути листьев + их значения (raw). Возвращает dict path->value."""
    # найти стартовый объект: { ... } верхнего уровня
    start = text.find('{')
    depth, i = 0, start
    while i < len(text):
        c = text[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: break
        i += 1
    body = text[start+1:i]
    out = {}
    def walk(s, prefix):
        # парсим ключи на текущем уровне
        pos = 0
        while pos < len(s):
            m = re.match(r'\s*([A-Za-z_][A-Za-z0-9_]*|\'[^\']*\'|\"[^\"]*\")\s*:', s[pos:])
            if not m:
                # пропустить до следующей строки с ключом: ищем следующий ': ' на уровне 0
                nxt = re.search(r'[\'\"]?[A-Za-z_][A-Za-z0-9_]*[\'\"]?\s*:', s[pos:])
                if not nxt: break
                pos += nxt.start()
                continue
            key = m.group(1).strip('\'"')
            pos += m.end()
            # значение: до конца (строка/функция/объект)
            if pos < len(s) and s[pos] in ' \t':
                pos = len(s) - len(s[pos:].lstrip())
            if pos < len(s) and s[pos] == '{':
                d, j = 1, pos+1
                while j < len(s) and d:
                    if s[j] == '{': d += 1
                    elif s[j] == '}': d -= 1
                    j += 1
                val = s[pos:j]
                path = f'{prefix}{key}'
                # вложенные ключи
                walk(s[pos+1:j-1], path + '.')
                out[path] = '<obj>'
                pos = j
            else:
                # скаляр/функция: до запятой на уровне 0
                j, d = pos, 0
                while j < len(s):
                    c = s[j]
                    if c in '({[': d += 1
                    elif c in ')}]':
                        if d == 0: break
                        d -= 1
                    elif c == ',' and d == 0: break
                    j += 1
                out[f'{prefix}{key}'] = s[pos:j].strip()
                pos = j + 1 if j < len(s) and s[j] == ',' else j
    walk(body, '')
    return out

en = parse_keys(open('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts', encoding='utf-8').read())
ru = parse_keys(open('/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/ru.ts', encoding='utf-8').read())
print(f'en листьев: {len(en)}, ru листьев: {len(ru)}')
missing = [k for k in en if k not in ru]
extra = [k for k in ru if k not in en]
print(f'MISSING в ru: {len(missing)}')
for k in sorted(missing): print(f'  {k}  = {en[k][:70]!r}')
print(f'ЛИШНИЕ в ru: {len(extra)}')
for k in sorted(extra)[:10]: print(f'  {k}')
