#!/usr/bin/env python3
"""
Structural merge: insert translations from translations_table.json into ru.ts.

Strategy:
1. Parse ru.ts into blocks (key line + all following non-key lines)
2. Parse en.ts to get canonical key order (for correct insertion position)
3. For each key in the table:
   a. If key exists in ru.ts with English value → replace value
   b. If key is missing from ru.ts → insert block at correct position
4. Write output, preserving existing translations and formatting
"""
import json, re, sys
from pathlib import Path

MOD_DIR = Path(r'C:\Users\covhnw\AppData\Local\hermes\desktop-ru-mod')
RU_TS = MOD_DIR / 'i18n' / 'ru.ts'
EN_TS = Path(r'C:\Users\covhnw\AppData\Local\hermes\hermes-agent\apps\desktop\src\i18n\en.ts')
TABLE_JSON = MOD_DIR / 'translations_table.json'
BACKUP = MOD_DIR / 'i18n' / 'ru.ts.bak'

# --- Load data ---
with open(RU_TS, 'r', encoding='utf-8') as f:
    ru_text = f.read()
with open(EN_TS, 'r', encoding='utf-8') as f:
    en_text = f.read()
with open(TABLE_JSON, 'r', encoding='utf-8') as f:
    table = json.load(f)

# --- Parse helpers ---
KEY_RE = re.compile(
    r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))\s*:\s*(?P<rest>.*?)$"
)

def is_english_value(value_str):
    """Check if a leaf value is in English (not translated)."""
    if not value_str:
        return False
    # Skip function values, references, template strings with interpolation
    if value_str.startswith('(') or '=>' in value_str:
        # Check if the function body contains Russian
        if re.search(r'[А-ЯЁа-яё]', value_str):
            return False
        return True
    # Remove quotes
    inner = value_str.strip()
    if (inner.startswith("'") and inner.endswith("'")) or \
       (inner.startswith('"') and inner.endswith('"')) or \
       (inner.startswith('`') and inner.endswith('`')):
        inner = inner[1:-1]
    # Contains Cyrillic = translated
    if re.search(r'[А-ЯЁа-яё]', inner):
        return False
    # Starts with capital letter or common English words = untranslated
    return bool(re.match(r'^[A-Z]', inner))

def parse_blocks(text):
    """Parse text into list of (indent, key, path, lines, is_object)."""
    blocks = []
    lines = text.split('\n')
    stack = []  # (indent, key)
    i = 0
    
    while i < len(lines):
        line = lines[i]
        m = KEY_RE.match(line)
        
        if m:
            indent_str = m.group('indent')
            indent = len(indent_str)
            key = m.group('word') or m.group('sq') or m.group('dq') or m.group('num')
            rest = m.group('rest').strip()
            
            # Pop stack
            while stack and stack[-1][0] >= indent:
                stack.pop()
            
            # Build path
            path = '.'.join([k for _, k in stack] + [key])
            
            # Check if object (ends with {)
            is_obj = rest == '{'
            
            # Collect all lines belonging to this block
            block_lines = [line]
            if is_obj:
                # Find closing brace at same indent
                j = i + 1
                depth = 1
                while j < len(lines) and depth > 0:
                    l = lines[j]
                    block_lines.append(l)
                    # Count braces (rough)
                    depth += l.count('{') - l.count('}')
                    j += 1
                i = j - 1
            else:
                # Single-line value (might be multi-line template string)
                j = i + 1
                while j < len(lines) and not KEY_RE.match(lines[j]) and lines[j].strip():
                    block_lines.append(lines[j])
                    j += 1
                i = j - 1
            
            blocks.append({
                'indent': indent,
                'key': key,
                'path': path,
                'lines': block_lines,
                'is_object': is_obj,
                'line_idx': i - len(block_lines) + 1,
            })
            
            if is_obj:
                stack.append((indent, key))
        
        i += 1
    
    return blocks

def get_en_key_order(en_text):
    """Get the canonical key order from en.ts (for correct insertion position)."""
    blocks = parse_blocks(en_text)
    # For each parent path, record child key order
    order = {}
    for b in blocks:
        parts = b['path'].rsplit('.', 1)
        parent = parts[0] if len(parts) > 1 else ''
        child = parts[-1] if len(parts) > 1 else b['path']
        if parent not in order:
            order[parent] = []
        if child not in order[parent]:
            order[parent].append(child)
    return order

# --- Parse both files ---
ru_blocks = parse_blocks(ru_text)
en_order = get_en_key_order(en_text)

# Build path → block index map for ru.ts
ru_path_to_idx = {}
for idx, b in enumerate(ru_blocks):
    ru_path_to_idx[b['path']] = idx

# --- Phase 1: Find actionable keys ---
to_replace = []  # (path, old_block_idx, new_value_str)
to_insert = []   # (parent_path, key_name, new_value_str)
skipped_no_table = []
skipped_already_translated = []

for table_path, translation in table.items():
    if not translation or not translation.strip():
        skipped_no_table.append(table_path)
        continue
    
    # Clean translation value
    trans = translation.strip()
    # Remove outer quotes if present (table stores values with quotes)
    if (trans.startswith("'") and trans.endswith("'")) or \
       (trans.startswith('"') and trans.endswith('"')):
        trans = trans[1:-1]
    
    # Escape single quotes for TS
    escaped = trans.replace("'", "\\'")
    new_val = f"'{escaped}'"
    
    if table_path in ru_path_to_idx:
        # Key exists in ru.ts — check if untranslated
        idx = ru_path_to_idx[table_path]
        block = ru_blocks[idx]
        if not block['is_object']:
            # Get current value
            first_line = block['lines'][0]
            m = KEY_RE.match(first_line)
            if m:
                current_val = m.group('rest').strip().rstrip(',')
                if is_english_value(current_val):
                    to_replace.append((table_path, idx, new_val))
                else:
                    skipped_already_translated.append(table_path)
    else:
        # Key missing — insert
        parts = table_path.rsplit('.', 1)
        parent = parts[0] if len(parts) > 1 else ''
        key_name = parts[-1] if len(parts) > 1 else table_path
        to_insert.append((parent, key_name, new_val))

print(f"=== План мерджа ===")
print(f"  Заменить (English → Русский): {len(to_replace)}")
print(f"  Вставить (отсутствуют):     {len(to_insert)}")
print(f"  Пропущено (уже переведено): {len(skipped_already_translated)}")
print(f"  Пропущено (нет перевода):   {len(skipped_no_table)}")

if len(to_replace) == 0 and len(to_insert) == 0:
    print("\nНечего менять — переводы уже вставлены или таблица пуста.")
    sys.exit(0)

# --- Phase 2: Build output ---
lines = ru_text.split('\n')
changes = 0

# 2a: Replace English values with Russian translations
# Work backwards to preserve indices
for path, idx, new_val in sorted(to_replace, key=lambda x: -x[1]):
    block = ru_blocks[idx]
    first_line = block['lines'][0]
    m = KEY_RE.match(first_line)
    if m:
        indent = m.group('indent')
        key_part = first_line[:m.start('rest')]
        rest = m.group('rest').strip().rstrip(',')
        comma = ',' if first_line.rstrip().endswith(',') else ''
        new_line = f"{key_part}{new_val}{comma}"
        # Replace the first line
        line_idx = block['line_idx']
        lines[line_idx] = new_line
        changes += 1

# 2b: Insert missing keys
# Sort by parent path + key order for correct placement
def insert_sort_key(item):
    parent, key_name, _ = item
    # Find where this key should go based on en.ts order
    if parent in en_order and key_name in en_order[parent]:
        pos = en_order[parent].index(key_name)
    else:
        pos = 9999
    return (parent, pos)

to_insert_sorted = sorted(to_insert, key=insert_sort_key)

# Group by parent for batch insertion
from collections import defaultdict
inserts_by_parent = defaultdict(list)
for parent, key_name, new_val in to_insert_sorted:
    inserts_by_parent[parent].append((key_name, new_val))

for parent, children in inserts_by_parent.items():
    # Find the parent block in ru.ts
    parent_parts = parent.split('.')
    
    # Find the parent object in ru_blocks
    parent_block = None
    parent_idx = ru_path_to_idx.get(parent)
    if parent_idx is not None:
        parent_block = ru_blocks[parent_idx]
    
    if parent_block is None or not parent_block['is_object']:
        # Parent doesn't exist in ru.ts — need to create it
        # For now, skip (complex case)
        print(f"  [~] Пропущена вставка в '{parent}' — родитель не найден")
        continue
    
    # Find the closing brace line of the parent
    parent_start = parent_block['line_idx']
    parent_lines = parent_block['lines']
    # Find the last line (closing brace)
    close_line_idx = parent_start + len(parent_lines) - 1
    close_line = lines[close_line_idx]
    close_indent = len(close_line) - len(close_line.lstrip())
    
    # Get existing children order from en.ts
    ordered_children = en_order.get(parent, [])
    
    # Determine insert position: after the last existing child that comes before in en order
    existing_children = []
    for b in ru_blocks:
        if b['path'].startswith(parent + '.') and b['path'].count('.') == parent.count('.') + 1:
            key = b['key']
            pos = ordered_children.index(key) if key in ordered_children else 9999
            existing_children.append((pos, b))
    
    existing_children.sort()
    
    # Build insertion lines
    child_indent = close_indent  # Same indent as closing brace = 2 levels
    insert_lines = []
    for key_name, new_val in children:
        insert_lines.append(f"{' ' * child_indent}{key_name}: {new_val},")
    
    # Insert before the closing brace
    insert_pos = close_line_idx
    for line in reversed(insert_lines):
        lines.insert(insert_pos, line)
    changes += len(children)

# --- Phase 3: Write output ---
# Backup
with open(BACKUP, 'w', encoding='utf-8') as f:
    f.write(ru_text)
print(f"\n  Бэкап: {BACKUP}")

# Write updated
output = '\n'.join(lines)
with open(RU_TS, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"  Записано: {RU_TS}")
print(f"  Строк: было {len(ru_text.split(chr(10)))}, стало {len(lines)} (+{len(lines) - len(ru_text.split(chr(10)))})")
print(f"  Всего изменений: {changes}")
print("\nГОТОВО. Проверь сборку: cd apps/desktop && npm run build")
