#!/usr/bin/env python3
"""Рекогносцировка фазы 8: какие из 135 warment-строк (вынесенный хардкод)
реально существуют в актуальном src как хардкод."""
import json, os, re

keys = json.load(open('/home/covhnw/projects/hermes-desktop-ru/warment_added_keys.json'))
SRC = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src'

def clean(val):
    """Значение en → строка для поиска (убрать кавычки/обёртку)."""
    v = val.strip()
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    if v.startswith('`') and v.endswith('`'):
        return v[1:-1]
    return v

# индексируем все tsx/ts файлы (кроме i18n/)
files = []
for root, dirs, fnames in os.walk(SRC):
    if 'i18n' in root or 'node_modules' in root:
        continue
    for f in fnames:
        if f.endswith(('.tsx', '.ts')):
            files.append(os.path.join(root, f))

found = {}   # key -> [files]
not_found = []
for key, info in keys.items():
    needle = clean(info.get('en', ''))
    if len(needle) < 8:
        not_found.append((key, 'короткое значение'))
        continue
    hits = []
    for f in files:
        try:
            content = open(f, encoding='utf-8').read()
        except Exception:
            continue
        # ищем как строковый литерал (в кавычках или backtick)
        if needle in content:
            hits.append(f.replace(SRC + '/', ''))
    if hits:
        found[key] = hits
    else:
        not_found.append((key, needle[:60]))

print(f'НАЙДЕНО в актуальном коде: {len(found)} из {len(keys)}')
print(f'НЕ найдено (изменились/удалены): {len(not_found)}')
print()
print('=== найденные (ключ → файлы) ===')
for key, hits in sorted(found.items()):
    print(f'{key}  →  {", ".join(sorted(set(hits))[:3])}')
