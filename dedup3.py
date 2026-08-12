#!/usr/bin/env python3
"""Дедоп-3: для каждого пути — вырезать инлайн-ключи из его строки, если их путь существует."""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'ru.ts'
lines = open(path, encoding='utf-8').read().splitlines()

def leaf_all(lines):
    stack, out, i = [], {}, 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*|'[^']*'):\s*(.*)$", line)
        if m:
            indent = len(m.group(1))
            while stack and stack[-1][1] >= indent:
                stack.pop()
            rest = m.group(3).rstrip()
            if rest.endswith('{'):
                stack.append((m.group(2).strip("'"), indent))
                i += 1
                continue
            path_ = '.'.join(s[0] for s in stack + [(m.group(2).strip("'"), indent)])
            j = i
            depth = 0
            while j < len(lines):
                s = lines[j]
                depth += s.count('(') + s.count('{') + s.count('[') - s.count(')') - s.count('}') - s.count(']')
                if depth <= 0 and (j > i or s.rstrip().endswith(',')):
                    break
                j += 1
            out[path_] = (i, j, indent)
            i = j + 1
            continue
        i += 1
    return out

paths = leaf_all(lines)
cut = 0
for p, (i, j, ind) in list(paths.items()):
    s = lines[i]
    # цикл по ВСЕМ инлайн-ключам строки (после первого ключа)
    pos = 0
    while True:
        m = re.search(r",\s*([A-Za-z_][A-Za-z0-9_]*):", s[pos:])
        if not m:
            break
        key2 = m.group(1)
        q = p.rsplit('.', 1)[0] + '.' + key2 if '.' in p else key2
        if q in paths and q != p:
            m2 = re.match(r"\s*" + re.escape(key2) + r":.*?($|,(?=\s*[A-Za-z_]))", s[pos + m.start(1):], re.S)
            if m2:
                s = s[:pos + m.start(1)] + (m2.group(1) or '')
                cut += 1
                print(f'  вырезано [{q}] из строки {i+1}')
                continue  # строка изменилась — ищем с той же позиции
        pos += m.end()
    lines[i] = s

open(path, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'инлайн-вырезок: {cut}')
