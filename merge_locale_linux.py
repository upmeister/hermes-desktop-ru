"""Merge: en.ts (структура) + ru.ts (существующие переводы) + translations_final.json."""
import re, json
from pathlib import Path

SOURCE = Path("/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts")
TARGET = Path("/home/covhnw/projects/hermes-desktop-ru/i18n/ru.ts")
TRANSLATIONS = Path("/home/covhnw/projects/hermes-desktop-ru/translations_final.json")
OVERRIDES = Path("/home/covhnw/projects/hermes-desktop-ru/translations_override.json")

KEY_RE = re.compile(
    r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))"
    r"\s*:\s*(?P<rest>.*?)\s*$"
)


def parse(lines):
    stack = []
    blocks = []
    current = None
    children = {}  # parent_path -> [blocks] (в порядке появления)
    for line in lines:
        km = KEY_RE.match(line)
        indent = len(re.match(r'^(\s*)', line).group(1))
        if km:
            key = km.group('word') or km.group('sq') or km.group('dq') or km.group('num')
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = '.'.join(s[1] for s in stack)
            stack.append((indent, key))
            path = '.'.join(s[1] for s in stack)
            rest = km.group('rest')
            is_object = rest.rstrip().endswith('{')
            if km.group('word'):
                key_token = km.group('word')
            elif km.group('sq'):
                key_token = f"'{km.group('sq')}'"
            elif km.group('dq'):
                key_token = f'"{km.group("dq")}"'
            else:
                key_token = km.group('num')
            blocks.append({
                'indent': indent, 'path': path, 'key_token': key_token,
                'rest': rest, 'is_object': is_object, 'lines': [line],
            })
            children.setdefault(parent, []).append(blocks[-1])
            current = len(blocks) - 1
        else:
            if current is not None:
                blocks[current]['lines'].append(line)
    return blocks, children


def get_child_paths(en_blocks, parent_path, children):
    return children.get(parent_path, [])


def emit_leaf_lines(ru_block):
    lines = ru_block['lines']
    indent = ru_block['indent']
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped in ('},', '}'):
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= indent:
                break
        result.append(line)
    if result:
        last = result[-1].rstrip()
        if last and not last.endswith(',') and not last.endswith('{') and not last.endswith(':'):
            result[-1] = last + ',\n'
    return result


def emit_block(b, en_blocks, ru_map, en_map, T, out, en_children):
    ru = ru_map.get(b['path'])
    indent_str = ' ' * b['indent']
    key = b['key_token']

    if b['is_object']:
        out.append(f"{indent_str}{key}: {{\n")
        for child in get_child_paths(en_blocks, b['path'], en_children):
            emit_block(child, en_blocks, ru_map, en_map, T, out, en_children)
        out.append(f"{indent_str}}},\n")
        return

    if ru is not None and not ru['is_object'] and b['path'] not in OVERRIDE:
        out.extend(emit_leaf_lines(ru))
        return

    if b['path'] in T:
        val = T[b['path']]
        if '\n' in val:
            parts = val.split('\n')
            out.append(f"{indent_str}{key}: {parts[0]}\n")
            cont = ' ' * (b['indent'] + 8)
            for p in parts[1:]:
                out.append(f"{cont}{p}\n")
            # multi-line: запятая к последней строке, если её нет
            last = out[-1].rstrip()
            if last and not last.endswith(',') and not last.endswith('{'):
                out[-1] = last + ',\n'
        else:
            out.append(f"{indent_str}{key}: {val},\n")
        return

    en_block = en_map.get(b['path'])
    if en_block:
        for line in en_block['lines']:
            stripped = line.strip()
            if stripped in ('},', '}') and len(line) - len(line.lstrip()) <= b['indent']:
                break
            out.append(line)
        last = out[-1].rstrip()
        if last and not last.endswith(',') and not last.endswith('{') and not last.endswith(':'):
            out[-1] = last + ',\n'


def main():
    T = json.loads(TRANSLATIONS.read_text(encoding='utf-8'))
    global OVERRIDE
    OVERRIDE = set(json.loads(OVERRIDES.read_text(encoding='utf-8'))) if OVERRIDES.exists() else set()
    en_lines = SOURCE.read_text(encoding='utf-8').splitlines(keepends=True)
    ru_lines = TARGET.read_text(encoding='utf-8').splitlines(keepends=True)
    en_blocks, en_children = parse(en_lines)
    ru_blocks, _ = parse(ru_lines)
    ru_map = {b['path']: b for b in ru_blocks}
    en_map = {b['path']: b for b in en_blocks}

    prologue_end = 0
    for i, line in enumerate(ru_lines):
        if 'defineLocale(' in line:
            prologue_end = i
            break
    while prologue_end < len(ru_lines) and '{' not in ru_lines[prologue_end]:
        prologue_end += 1

    epilogue_start = len(ru_lines) - 1
    while epilogue_start >= 0:
        if ru_lines[epilogue_start].strip().startswith('})'):
            break
        epilogue_start -= 1

    out = list(ru_lines[:prologue_end + 1])
    for b in get_child_paths(en_blocks, '', en_children):
        emit_block(b, en_blocks, ru_map, en_map, T, out, en_children)
    out.extend(ru_lines[epilogue_start:])

    text = ''.join(out)
    TARGET.write_text(text, encoding='utf-8')

    untranslated = sum(1 for b in en_blocks
                      if b['path'].count('.') >= 1
                      and b['path'] not in ru_map
                      and b['path'] not in T
                      and not b['is_object'])
    print(f"en_blocks={len(en_blocks)} ru_blocks={len(ru_blocks)} untranslated_leaves={untranslated}")
    print(f"Output lines: {len(out)}")
    if len(out) < len(en_lines) * 0.5:
        print("WARNING: Output much shorter than source — check is_object detection!")


if __name__ == '__main__':
    main()
