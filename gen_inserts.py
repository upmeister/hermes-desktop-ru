#!/usr/bin/env python3
"""Генерация вставок для en.ts/types.ts по 95 найденным хардкод-строкам warment.

Строит структуру {секция: {подсекция: {ключ: значение}}} и печатает:
1) фрагмент для en.ts (объект-литерал, TS-значения из warment en)
2) фрагмент для types.ts (интерфейс-структура)
3) ru-переводы → дополнение к translations_final.json
"""
import json, re

keys = json.load(open('/home/covhnw/projects/hermes-desktop-ru/warment_added_keys.json'))
# только найденные в коде (95) — список из рекогносцировки
import subprocess
out = subprocess.run(['python3', '/home/covhnw/projects/hermes-desktop-ru/recon_hardcode.py'],
                     capture_output=True, text=True).stdout
found_keys = set()
in_found = False
for line in out.splitlines():
    if line.startswith('=== найденные'):
        in_found = True
        continue
    if in_found and '  →  ' in line:
        found_keys.add(line.split('  →  ')[0].strip())

print(f'ключей для вставки: {len(found_keys)}')

def build_tree(paths_vals):
    tree = {}
    for p, v in paths_vals.items():
        parts = p.split('.')
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = v
    return tree

sel = {k: keys[k] for k in found_keys}
tree = build_tree({k: v['en'] for k, v in sel.items()})

def emit_ts(node, indent=2):
    lines = []
    for k, v in node.items():
        pad = ' ' * indent
        if isinstance(v, dict):
            lines.append(f'{pad}{k}: {{')
            lines.extend(emit_ts(v, indent + 2))
            lines.append(f'{pad}}},')
        else:
            lines.append(f'{pad}{k}: {v},')
    return lines

def emit_types(node, indent=2):
    lines = []
    for k, v in node.items():
        pad = ' ' * indent
        if isinstance(v, dict):
            lines.append(f'{pad}{k}: {{')
            lines.extend(emit_types(v, indent + 2))
            lines.append(f'{pad}}}')
        else:
            # функция или строка
            typ = 'string' if v.strip().startswith("'") or v.strip().startswith('"') else '(…args) => string'
            lines.append(f'{pad}{k}: {typ}')
    return lines

en_frag = '\n'.join(emit_ts(tree))
types_frag = '\n'.join(emit_types(tree))

open('/home/covhnw/projects/hermes-desktop-ru/gen_en_fragment.txt', 'w').write(en_frag)
open('/home/covhnw/projects/hermes-desktop-ru/gen_types_fragment.txt', 'w').write(types_frag)
print('\n=== EN фрагмент (первые 60 строк) ===')
print('\n'.join(en_frag.splitlines()[:60]))
print(f'\n=== всего строк en: {len(en_frag.splitlines())}, types: {len(types_frag.splitlines())} ===')
