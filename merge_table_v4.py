#!/usr/bin/env python3
"""
V4: Value-aware structural merge.
- Functions (=>) → insert as raw code (no quotes)
- Object literals ({...}) → insert as raw code (no quotes)
- Plain strings → insert as 'escaped value' (handle internal quotes)
"""
import json, re
from pathlib import Path
from collections import defaultdict

MOD_DIR = Path(r'C:\Users\covhnw\AppData\Local\hermes\desktop-ru-mod')
RU_TS = MOD_DIR / 'i18n' / 'ru.ts'
EN_TS = Path(r'C:\Users\covhnw\AppData\Local\hermes\hermes-agent\apps\desktop\src\i18n\en.ts')
TABLE_JSON = MOD_DIR / 'translations_table.json'
PRE_MERGE = MOD_DIR / 'i18n' / 'ru.ts.premerge'

# Restore from original
ru_text = PRE_MERGE.read_text('utf-8')
en_text = EN_TS.read_text('utf-8')
table = json.loads(TABLE_JSON.read_text('utf-8'))

KEY_RE = re.compile(
    r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\")\s*:\s*(?P<rest>.*?)$"
)

# === Parse helpers ===
def parse_keys(text):
    lines = text.split('\n')
    result = []
    stack = []
    for idx, line in enumerate(lines):
        m = KEY_RE.match(line)
        if not m: continue
        indent = len(m.group('indent'))
        key = m.group('word') or m.group('sq') or m.group('dq')
        rest = m.group('rest').strip().rstrip(',')
        is_obj = (rest == '{')
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = '.'.join([k for _, k in stack] + [key])
        result.append((idx, indent, key, path, is_obj))
        if is_obj:
            stack.append((indent, key))
    return result

en_keys = parse_keys(en_text)
ru_keys = parse_keys(ru_text)

en_order = defaultdict(list)
for _, _, key, path, _ in en_keys:
    parts = path.rsplit('.', 1)
    if len(parts) == 2:
        parent, child = parts
        if child not in en_order[parent]:
            en_order[parent].append(child)

ru_path_to_line = {}
ru_path_to_indent = {}
for line_idx, indent, key, path, is_obj in ru_keys:
    ru_path_to_line[path] = line_idx
    ru_path_to_indent[path] = indent

ru_paths = set(ru_path_to_line.keys())

# === Value classification ===
def classify_value(raw):
    """Return ('func', code) | ('object', code) | ('string', escaped_str)"""
    v = raw.strip()
    # Remove outer quotes for inspection
    inner = v
    if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
        inner = v[1:-1]
    
    # Check if it's an arrow function
    if '=>' in inner:
        return ('func', inner)
    
    # Check if it's an object literal
    if inner.startswith('{') and inner.endswith('}'):
        return ('object', inner)
    
    # It's a plain string — escape single quotes
    escaped = inner.replace("\\", "\\\\").replace("'", "\\'")
    return ('string', f"'{escaped}'")

# === Find value end line (for multi-line awareness) ===
def get_value_end_line(lines, key_line_idx, key_indent):
    j = key_line_idx + 1
    while j < len(lines):
        l = lines[j]
        if not l.strip():
            j += 1
            continue
        if l.strip().startswith('//'):
            j += 1
            continue
        l_indent = len(l) - len(l.lstrip())
        if l_indent <= key_indent:
            break
        if KEY_RE.match(l):
            break
        j += 1
    return j - 1

ru_lines_orig = ru_text.split('\n')

# === Build existing children with end lines ===
children_end_lines = defaultdict(list)

for line_idx, indent, key, path, is_obj in ru_keys:
    parts = path.rsplit('.', 1)
    if len(parts) == 2:
        p, c = parts
        if is_obj:
            end = line_idx
            for j in range(line_idx + 1, len(ru_lines_orig)):
                l = ru_lines_orig[j]
                l_indent = len(l) - len(l.lstrip())
                if l.strip() == '}' and l_indent <= indent:
                    end = j
                    break
        else:
            end = get_value_end_line(ru_lines_orig, line_idx, indent)
        
        order = en_order.get(p, [])
        try:
            pos = order.index(c)
        except ValueError:
            pos = 9999
        children_end_lines[p].append((c, end, pos))

# === Process insertions ===
inserts_at_line = defaultdict(list)
stats = {'func': 0, 'object': 0, 'string': 0, 'skipped_no_parent': 0, 'skipped_exists': 0}

for table_path, translation in table.items():
    if not translation or not translation.strip():
        continue
    if table_path in ru_paths:
        stats['skipped_exists'] += 1
        continue
    
    parts = table_path.rsplit('.', 1)
    if len(parts) < 2:
        continue
    parent, key_name = parts
    if parent not in ru_paths:
        stats['skipped_no_parent'] += 1
        continue
    
    vtype, code = classify_value(translation)
    child_indent = ru_path_to_indent[parent] + 2
    
    if vtype == 'func':
        line = f"{' ' * child_indent}{key_name}: {code},"
        stats['func'] += 1
    elif vtype == 'object':
        line = f"{' ' * child_indent}{key_name}: {code},"
        stats['object'] += 1
    else:  # string
        line = f"{' ' * child_indent}{key_name}: {code},"
        stats['string'] += 1
    
    # Find insertion anchor
    order = en_order.get(parent, [])
    try:
        pos = order.index(key_name)
    except ValueError:
        pos = 9999
    
    existing = children_end_lines.get(parent, [])
    insert_after = ru_path_to_line[parent]
    for ek, e_end, epos in existing:
        if epos < pos:
            insert_after = max(insert_after, e_end)
    
    inserts_at_line[insert_after + 1].append(line)

# === Apply insertions ===
ru_lines = list(ru_lines_orig)
for anchor in sorted(inserts_at_line.keys(), reverse=True):
    for line in reversed(inserts_at_line[anchor]):
        ru_lines.insert(anchor, line)

# === Write output ===
bak = RU_TS.with_name('ru.ts.bak5')
bak.write_text(ru_text, 'utf-8')

output = '\n'.join(ru_lines)
RU_TS.write_text(output, 'utf-8')

# === Report ===
print(f"Исходный ru.ts: {len(ru_text.splitlines())} строк")
print(f"Обновлённый:     {len(ru_lines)} строк (+{len(ru_lines) - len(ru_text.splitlines())})")
print(f"\nВставлено ключей: {sum(stats[k] for k in ['func','object','string'])}")
print(f"  🔴 Функций (без кавычек):  {stats['func']}")
print(f"  🔴 Объектов (без кавычек): {stats['object']}")
print(f"  ⚪ Строк (с кавычками):    {stats['string']}")
print(f"\nПропущено:")
print(f"  ⏭️  Уже есть в ru.ts:      {stats['skipped_exists']}")
print(f"  ⏭️  Нет родителя в ru.ts:  {stats['skipped_no_parent']}")

# Quick validation
print(f"\n=== Валидация ===")
# Check a function insertion
for line in ru_lines:
    if 'resumeWhenBackgroundDone' in line:
        print(f"  resumeWhenBackgroundDone: {line.strip()[:100]}")
        break

print(f"\nБэкап: {bak}")
print(f"Готово: {RU_TS}")
