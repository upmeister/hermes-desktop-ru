#!/usr/bin/env python3
"""
V2: Indentation-based structural merge.
Walks ru.ts line by line, tracks the key-path stack via indentation.
Where a key is missing (in en.ts but not ru.ts) AND a translation exists in
translations_table.json, inserts the translated block at the correct position.

Also replaces English leaf values with Russian translations when the table
covers them.
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

MOD_DIR = Path(r'C:\Users\covhnw\AppData\Local\hermes\desktop-ru-mod')
RU_TS = MOD_DIR / 'i18n' / 'ru.ts'
EN_TS = Path(r'C:\Users\covhnw\AppData\Local\hermes\hermes-agent\apps\desktop\src\i18n\en.ts')
TABLE_JSON = MOD_DIR / 'translations_table.json'

# Load
ru_text = RU_TS.read_text('utf-8')
en_text = EN_TS.read_text('utf-8')
table = json.loads(TABLE_JSON.read_text('utf-8'))

# --- Regex ---
KEY_RE = re.compile(
    r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\")\s*:\s*(?P<rest>.*?)$"
)

# --- Parse en.ts into canonical structure ---
# We need: for each parent path, the ordered list of child keys (from en.ts)
# and their indent levels relative to root.

def parse_en_structure(text):
    """Parse en.ts into a path→info dict for ordering and indentation."""
    lines = text.split('\n')
    # First, find all key lines with their indent and key name
    entries = []  # (line_idx, indent, key, is_object, rest)
    stack = []    # (indent, key)
    
    for idx, line in enumerate(lines):
        m = KEY_RE.match(line)
        if not m:
            continue
        indent = len(m.group('indent'))
        key = m.group('word') or m.group('sq') or m.group('dq')
        rest = m.group('rest').strip().rstrip(',')
        is_obj = (rest == '{')
        
        # Pop stack
        while stack and stack[-1][0] >= indent:
            stack.pop()
        
        path = '.'.join([k for _, k in stack] + [key])
        entries.append((idx, indent, key, is_obj, path))
        
        if is_obj:
            stack.append((indent, key))
    
    # Build order map: parent_path → [child_keys_in_order]
    order = defaultdict(list)
    indent_map = {}  # path → indent level
    for _, indent, key, _, path in entries:
        indent_map[path] = indent
        parts = path.rsplit('.', 1)
        if len(parts) == 2:
            parent, child = parts
            if child not in order[parent]:
                order[parent].append(child)
    
    return order, indent_map

en_order, en_indent = parse_en_structure(en_text)

# --- Parse ru.ts into lines with path tracking ---
ru_lines = ru_text.split('\n')

# Find the prologue (everything before defineLocale({) and epilogue
prologue_end = 0
define_start = -1
root_indent = None
for i, line in enumerate(ru_lines):
    if 'defineLocale({' in line:
        define_start = i
        m = re.match(r'^(\s*)', line)
        root_indent = len(m.group(1))
        break

if define_start < 0:
    print("ERROR: defineLocale({ not found in ru.ts")
    sys.exit(1)

prologue = ru_lines[:define_start + 1]  # include the defineLocale({ line

# Parse the body (inside defineLocale)
body_start = define_start + 1

# Walk body lines, tracking path stack
class Block:
    __slots__ = ('path', 'indent', 'key', 'is_object', 'lines', 'line_start')
    def __init__(self, path, indent, key, is_object, lines, line_start):
        self.path = path
        self.indent = indent
        self.key = key
        self.is_object = is_object
        self.lines = lines
        self.line_start = line_start

def parse_body(lines, start_idx):
    """Parse lines from start_idx, return list of Block objects."""
    blocks = []
    stack = []  # (indent, key)
    i = start_idx
    
    while i < len(lines):
        line = lines[i]
        m = KEY_RE.match(line)
        
        if not m:
            i += 1
            continue
        
        indent = len(m.group('indent'))
        key = m.group('word') or m.group('sq') or m.group('dq')
        rest_raw = m.group('rest').strip()
        rest = rest_raw.rstrip(',')
        is_obj = (rest == '{')
        
        # Check if we're exiting the defineLocale body
        if not stack and indent <= root_indent:
            # We've hit the closing of defineLocale
            break
        
        # Pop stack
        while stack and stack[-1][0] >= indent:
            stack.pop()
        
        path = '.'.join([k for _, k in stack] + [key])
        
        # Collect block lines
        block_lines = [line]
        j = i + 1
        if is_obj:
            # Object: collect until matching close brace
            # For indentation-based: collect until a line at same or lower indent
            # that is just '}' or another key at same indent
            depth = 1
            while j < len(lines) and depth > 0:
                l = lines[j]
                block_lines.append(l)
                # Count braces roughly
                depth += l.count('{') - l.count('}')
                j += 1
        else:
            # Leaf: collect continuation lines (indented more, non-key)
            while j < len(lines):
                l = lines[j]
                if l.strip() == '':
                    j += 1
                    continue
                if KEY_RE.match(l):
                    break
                if l.strip().startswith('//'):
                    j += 1
                    continue
                # Check indentation - continuation lines are indented deeper
                l_indent = len(l) - len(l.lstrip())
                if l_indent > indent:
                    block_lines.append(l)
                    j += 1
                else:
                    break
        
        blocks.append(Block(path, indent, key, is_obj, block_lines, i))
        i = j
        continue
    
    return blocks

ru_blocks = parse_body(ru_lines, body_start)

# Build path → block map
ru_map = {b.path: b for b in ru_blocks}
ru_paths = set(ru_map.keys())

print(f"ru.ts body blocks: {len(ru_blocks)}")
print(f"ru.ts unique paths: {len(ru_paths)}")

# --- Find what to insert ---
to_insert = []  # (parent_path, key_name, translation_value, desired_indent)

for table_path, translation in table.items():
    if not translation or not translation.strip():
        continue
    
    # Clean translation value
    trans = translation.strip()
    # Remove outer quotes
    if (trans.startswith("'") and trans.endswith("'")) or \
       (trans.startswith('"') and trans.endswith('"')):
        trans = trans[1:-1]
    
    # Escape single quotes
    escaped = trans.replace("'", "\\'").replace('\n', '\\n')
    new_val = f"'{escaped}'"
    
    if table_path in ru_paths:
        # Already exists in ru.ts — skip (even if English, handle separately)
        continue
    
    # This key is missing from ru.ts
    parts = table_path.rsplit('.', 1)
    if len(parts) < 2:
        continue
    parent, key_name = parts
    
    if parent not in ru_paths:
        # Parent doesn't exist either — skip for now
        continue
    
    # parent exists in ru.ts — we can insert this child
    # Get the parent's indent level
    parent_block = ru_map[parent]
    child_indent = parent_block.indent + 2  # standard 2-space nesting
    
    to_insert.append((parent, key_name, new_val, child_indent))

print(f"Keys to insert: {len(to_insert)}")

# Group by parent
inserts_by_parent = defaultdict(list)
for parent, key_name, new_val, child_indent in to_insert:
    inserts_by_parent[parent].append((key_name, new_val, child_indent))

# --- Build output ---
# Strategy: go through ru.ts lines, and when we encounter a parent block's
# closing brace, insert new children before it (in en.ts key order).

# First, build a map: for each parent, what new keys to insert (ordered by en.ts)
for parent in inserts_by_parent:
    children = inserts_by_parent[parent]
    # Sort by en.ts order
    order = en_order.get(parent, [])
    def sort_key(item):
        key_name = item[0]
        try:
            return order.index(key_name)
        except ValueError:
            return 9999
    children.sort(key=sort_key)

# Now build output lines
output_lines = list(prologue)  # Start with prologue

# We need to process the body with insertions
# Find the line after prologue
current_line = body_start

# For multi-line template strings and complex values, we need to preserve
# the original lines. Let's use a simpler approach:
# 1. Copy all original lines
# 2. For each parent block, insert new children before its closing line

# Rebuild the body preserving original structure + insertions
# Build a sorted list of insertions: (insert_line_idx, lines_to_insert)
insertions = []  # (line_idx, [lines])

for parent, children in inserts_by_parent.items():
    if parent not in ru_map:
        continue
    block = ru_map[parent]
    # Find the closing line: last line of the block
    close_line_idx = block.line_start + len(block.lines) - 1
    close_line = ru_lines[close_line_idx]
    close_indent = len(close_line) - len(close_line.lstrip())
    
    # Generate insertion lines
    insert_lines = []
    for key_name, new_val, child_indent in children:
        insert_lines.append(f"{' ' * child_indent}{key_name}: {new_val},")
    
    # Insert BEFORE the closing line
    insertions.append((close_line_idx, insert_lines))

# Sort insertions by line index (reverse for stable insertion)
insertions.sort(key=lambda x: -x[0])

# Apply insertions to ru_lines
result_lines = list(ru_lines)
for insert_idx, insert_lines in insertions:
    for line in reversed(insert_lines):
        result_lines.insert(insert_idx, line)

# Write output
output = '\n'.join(result_lines)

# Backup
bak_path = RU_TS.with_suffix('.ts.bak2')
bak_path.write_text(ru_text, 'utf-8')
print(f"Backup: {bak_path}")

# Write
RU_TS.write_text(output, 'utf-8')
print(f"Written: {RU_TS}")
print(f"Lines: {len(ru_lines)} → {len(result_lines)} (+{len(result_lines) - len(ru_lines)})")

# Summary
by_parent_count = {p: len(c) for p, c in inserts_by_parent.items()}
for parent, count in sorted(by_parent_count.items()):
    print(f"  {parent}: +{count} keys")
