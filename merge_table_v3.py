#!/usr/bin/env python3
"""
V3: Pure line-by-line merge. No block parsing — each key line is tracked
independently. Paths are built from an indent stack.

For each translated key in the table that is MISSING from ru.ts:
- Find its parent in ru.ts
- Insert a new line at the correct position (respecting en.ts key order)
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

MOD_DIR = Path(r'C:\Users\covhnw\AppData\Local\hermes\desktop-ru-mod')
RU_TS = MOD_DIR / 'i18n' / 'ru.ts'
EN_TS = Path(r'C:\Users\covhnw\AppData\Local\hermes\hermes-agent\apps\desktop\src\i18n\en.ts')
TABLE_JSON = MOD_DIR / 'translations_table.json'

ru_text = RU_TS.read_text('utf-8')
en_text = EN_TS.read_text('utf-8')
table = json.loads(TABLE_JSON.read_text('utf-8'))

KEY_RE = re.compile(
    r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\")\s*:\s*(?P<rest>.*?)$"
)

# === Phase 1: Parse en.ts → canonical order + indent levels ===
def parse_keys(text):
    """Return list of (line_idx, indent, key, path, is_object)."""
    lines = text.split('\n')
    result = []
    stack = []  # (indent, key)
    
    for idx, line in enumerate(lines):
        m = KEY_RE.match(line)
        if not m:
            continue
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

# Build en.ts order map
en_order = defaultdict(list)
en_indent = {}
for _, indent, key, path, _ in en_keys:
    en_indent[path] = indent
    parts = path.rsplit('.', 1)
    if len(parts) == 2:
        parent, child = parts
        if child not in en_order[parent]:
            en_order[parent].append(child)

# Build ru.ts maps
ru_path_to_line = {}   # path → line index in original text
ru_path_to_indent = {}
ru_path_is_obj = {}
for line_idx, indent, key, path, is_obj in ru_keys:
    ru_path_to_line[path] = line_idx
    ru_path_to_indent[path] = indent
    ru_path_is_obj[path] = is_obj

ru_paths = set(ru_path_to_line.keys())
print(f"en.ts paths: {len(en_keys)}")
print(f"ru.ts paths: {len(ru_keys)}")

# === Phase 2: Find keys to insert ===
Insertion = tuple  # (parent_path, key_name, translation_line, priority)
insertions = []

for table_path, translation in table.items():
    if not translation or not translation.strip():
        continue
    if table_path in ru_paths:
        continue  # Already exists
    
    # Clean translation
    trans = translation.strip()
    if (trans.startswith("'") and trans.endswith("'")) or \
       (trans.startswith('"') and trans.endswith('"')):
        trans = trans[1:-1]
    escaped = trans.replace("'", "\\'").replace('\n', '\\n')
    
    parts = table_path.rsplit('.', 1)
    if len(parts) < 2:
        continue
    parent, key_name = parts
    
    if parent not in ru_paths:
        continue  # Parent not found — skip
    
    # Determine indent: parent indent + 2
    child_indent = ru_path_to_indent[parent] + 2
    line = f"{' ' * child_indent}{key_name}: '{escaped}',"
    
    # Priority: position in en.ts order
    order = en_order.get(parent, [])
    try:
        pos = order.index(key_name)
    except ValueError:
        pos = 9999
    
    insertions.append((parent, key_name, line, pos, child_indent))

print(f"Keys to insert: {len(insertions)}")

# === Phase 3: Group by parent and determine insertion points ===
# For each parent, we need to find WHERE in the ru.ts lines to insert children.
# The insertion point is:
#   - After the last existing child that comes BEFORE in en.ts order
#   - Or after the parent's opening brace if no children before
#   - Or before the first existing child that comes AFTER in en.ts order

ru_lines = ru_text.split('\n')

# Build: for each parent, list of existing children with their line indices
children_of = defaultdict(list)  # parent → [(key_name, line_idx, order_pos)]
for line_idx, indent, key, path, is_obj in ru_keys:
    parts = path.rsplit('.', 1)
    if len(parts) == 2:
        p, c = parts
        order = en_order.get(p, [])
        try:
            pos = order.index(c)
        except ValueError:
            pos = 9999
        children_of[p].append((c, line_idx, pos))

# For each parent with insertions, find the exact line to insert before
# We need to modify lines in reverse order to keep indices stable
line_mods = []  # (insert_before_line_idx, [lines_to_insert])

for parent, children in sorted(insertions, key=lambda x: inserts_by_parent_key(x)):
    pass

# Better approach: group insertions by parent, then for each parent,
# find insertion point

inserts_by_parent = defaultdict(list)
for parent, key_name, line, pos, child_indent in insertions:
    inserts_by_parent[parent].append((key_name, line, pos))

# For each parent, determine the insertion anchor line
all_inserts = []  # (anchor_line_idx, [lines])

for parent, items in inserts_by_parent.items():
    items.sort(key=lambda x: x[2])  # Sort by en.ts order position
    
    # Get existing children of this parent
    existing = children_of.get(parent, [])
    existing.sort(key=lambda x: x[2])  # Sort by en.ts order
    
    # For each item to insert, find where it goes
    for key_name, line, pos in items:
        # Find the last existing child with order < pos
        insert_after = -1
        for ek, eline, epos in existing:
            if epos < pos:
                insert_after = max(insert_after, eline)
        
        if insert_after < 0:
            # No children before — insert right after parent's opening line
            parent_line = ru_path_to_line[parent]
            insert_after = parent_line
        
        all_inserts.append((insert_after + 1, line))

# Group inserts at the same line
from collections import defaultdict
inserts_at_line = defaultdict(list)
for anchor, line in all_inserts:
    inserts_at_line[anchor].append(line)

# Sort by anchor line (descending for stable insertion)
for anchor in sorted(inserts_at_line.keys(), reverse=True):
    lines_to_insert = inserts_at_line[anchor]
    for line in reversed(lines_to_insert):
        ru_lines.insert(anchor, line)

# === Phase 4: Write output ===
# Backup
bak = RU_TS.with_name('ru.ts.bak3')
bak.write_text(ru_text, 'utf-8')

output = '\n'.join(ru_lines)
RU_TS.write_text(output, 'utf-8')

print(f"\nLines: {len(ru_text.split(chr(10)))} → {len(ru_lines)} (+{len(ru_lines) - len(ru_text.split(chr(10)))})")
print(f"Insertions: {len(insertions)} keys")
by_parent = defaultdict(int)
for p, _, _, _, _ in insertions:
    by_parent[p] += 1
for p, c in sorted(by_parent.items()):
    print(f"  {p}: +{c}")
print(f"\n✓ Written to {RU_TS}")
print(f"Backup: {bak}")
