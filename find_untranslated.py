#!/usr/bin/env python3
"""Найти в ru.ts значения, дословно совпадающие с en.ts (непереведённые)."""
import sys
sys.path.insert(0, '/home/covhnw/projects/hermes-desktop-ru')
from diff_keys2 import all_keys

BASE = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/'
en = all_keys(open(BASE + 'en.ts', encoding='utf-8').read())
ru = all_keys(open(BASE + 'ru.ts', encoding='utf-8').read())

untranslated = []
for k in en:
    if k in ru and ru[k] == en[k] and en[k] not in ('<obj>', '<q>') and en[k]:
        # отсечь строки без текста (цифры, пустые)
        v = en[k].strip().strip("'").strip('`')
        if v and not v.isdigit() and not v.startswith('path =>') and not v.startswith('('):
            untranslated.append((k, en[k]))

print(f'НЕПЕРЕВЕДЁННЫХ значений: {len(untranslated)}')
for k, v in untranslated:
    print(f'  {k} = {v[:90]!r}')
