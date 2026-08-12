#!/usr/bin/env python3
"""Удалить дубли ключей в ru.ts (вторые вхождения — строки или части инлайн-строк)."""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'ru.ts'
lines = open(path, encoding='utf-8').read().splitlines()

# 1) полные строки-дубли (первый ключ строки + путь) — удалить ВТОРОЕ вхождение
def first_key(line):
    m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*|'[^']*'):", line)
    return m.group(1).strip("'") if m else None

seen = {}
remove = set()
for i, ln in enumerate(lines):
    k = first_key(ln)
    if k:
        if k in seen:
            remove.add(i)
        else:
            seen[k] = i

# 2) инлайн-дубли: имя ключа встречается в ДРУГОЙ строке как «ключ:» (не первым)
#    — удалить ВТОРОЕ вхождение (подстроку с запятой)
import collections
key_occur = collections.defaultdict(list)
for i, ln in enumerate(lines):
    for m in re.finditer(r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*):", ln):
        key_occur[m.group(1)].append(i)

out = []
for i, ln in enumerate(lines):
    if i in remove:
        continue
    # инлайн-части: если строка содержит ключ, который уже был ПОЛНОЙ строкой ранее —
    # вырезать «, ключ: ...» до конца строки или до следующего ключа
    modified = ln
    for k, occ in key_occur.items():
        if len(occ) < 2:
            continue
        full_lines = [x for x in occ if x not in remove and first_key(lines[x]) == k]
        if not full_lines or i == full_lines[0]:
            continue  # это первый (канонический) — не трогаем
        # в этой строке ключ k встречается НЕ первым — вырезать фрагмент
        pat = re.compile(r",\s*" + re.escape(k) + r":.*?($|,(?=\s*[A-Za-z_]))")
        new = pat.sub(lambda m: m.group(1) or '', modified, count=1)
        if new != modified:
            modified = new
    out.append(modified)

open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'удалено полных строк-дублей: {len(remove)}')
