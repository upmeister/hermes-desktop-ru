#!/usr/bin/env python3
"""Точечная вставка недостающих ключей в en.ts и types.ts.

Для каждого нового пути находит deepest существующий контейнер-префикс
и вставляет недостающую ветку перед его закрывающей скобкой.
Пропускает пути, которые уже существуют.
"""
import json, re, sys

KEY_RE = re.compile(r"^(?P<indent>\s*)(?:(?P<word>\w+)|'(?P<sq>[^']+)'|\"(?P<dq>[^\"]+)\"|(?P<num>\d+))\s*:\s*(?P<rest>.*?)$")

def parse_blocks(lines):
    """Блоки: {path, indent, start (индекс строки ключа), end (индекс строки закрытия)}."""
    stack = []  # (indent, key, start)
    blocks = []
    for i, line in enumerate(lines):
        m = KEY_RE.match(line)
        if not m:
            continue
        indent = len(m.group('indent'))
        key = m.group('word') or m.group('sq') or m.group('dq') or m.group('num')
        rest = m.group('rest').rstrip()
        is_object = rest.endswith('{')
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = '.'.join(s[1] for s in stack) + ('.' if stack else '') + key
        stack.append((indent, key, i))
        if is_object:
            blocks.append({'path': path, 'indent': indent, 'start': i, 'end': None})
    # концы: для каждого блока-контейнера — строка закрытия = первая строка
    # с indent == block.indent, начинающаяся с '}'/'},' ПОСЛЕ start
    for b in blocks:
        for j in range(b['start'] + 1, len(lines)):
            l = lines[j]
            if not l.strip():
                continue
            m2 = re.match(r'^(\s*)(\}\},?|},?)$', l)
            if m2 and len(m2.group(1)) == b['indent']:
                b['end'] = j
                break
    return blocks

def existing_paths(blocks):
    return {b['path'] for b in blocks}

def deepest_parent(path, existing):
    """Самый длинный существующий префикс-путь (может быть leaf — ок для вставки)."""
    parts = path.split('.')
    for i in range(len(parts) - 1, 0, -1):
        cand = '.'.join(parts[:i])
        if cand in existing:
            return cand
    return None

def build_subtree(paths_vals, base):
    """Дерево новых веток относительно base: {сегмент: {...}|значение}."""
    tree = {}
    for p, v in paths_vals.items():
        parts = p.split('.')
        assert p.startswith(base + '.') or base == '', p
        rel = parts[len(base.split('.')) if base else 0:]
        node = tree
        for part in rel[:-1]:
            node = node.setdefault(part, {})
        node[rel[-1]] = v
    return tree

def render(node, indent, mode):
    """mode: 'en' (TS-литерал) или 'types' (интерфейс)."""
    out = []
    for k, v in node.items():
        pad = ' ' * indent
        if isinstance(v, dict):
            out.append(f'{pad}{k}: {{' if mode == 'en' else f'{pad}{k}: {{')
            out.extend(render(v, indent + 2, mode))
            out.append(f'{pad}}},' if mode == 'en' else f'{pad}}}')
        else:
            if mode == 'en':
                out.append(f'{pad}{k}: {v},')
            else:
                typ = 'string' if (v.strip().startswith("'") or v.strip().startswith('"')) else '(...args: unknown[]) => string'
                out.append(f'{pad}{k}: {typ}')
    return out

def insert(lines, blocks, parent_path, subtree, mode):
    """Вставить subtree в конец контейнера parent_path перед его закрытием."""
    parent = next(b for b in blocks if b['path'] == parent_path and b['end'] is not None)
    # indent детей = parent.indent + 2
    frag = render(subtree, parent['indent'] + 2, mode)
    # вставляем перед end
    lines[parent['end']:parent['end']] = [l + '\n' for l in frag]
    return lines

def main():
    mode = sys.argv[1]  # 'en' | 'types'
    file = sys.argv[2]
    new_keys = json.load(open('/home/covhnw/projects/hermes-desktop-ru/warment_added_keys.json'))

    lines = open(file, encoding='utf-8').read().splitlines(keepends=True)
    blocks = parse_blocks(lines)
    existing = existing_paths(blocks)

    # какие пути новые (для types передаём en-значение — нужно для определения типа)
    todo = {p: v['en'] for p, v in new_keys.items() if p not in existing}
    print(f'{mode}: новых путей: {len(todo)}')

    # группируем по deepest parent
    by_parent = {}
    for p in todo:
        parent = deepest_parent(p, existing)
        by_parent.setdefault(parent, {})[p] = todo[p]

    for parent, paths in sorted(by_parent.items(), key=lambda x: (x[0] is None, x[0] or '')):
        if parent is None:
            print(f'  ВНИМАНИЕ: нет родителя для: {list(paths)[:5]}')
            continue
        sub = build_subtree(paths, parent)
        lines = insert(lines, blocks, parent, sub, mode)
        blocks = parse_blocks(lines)  # пере-парсим после вставки
        existing = existing_paths(blocks)
        print(f'  вставлено в {parent}: {len(paths)} ключей')

    open(file, 'w', encoding='utf-8').writelines(lines)
    print(f'{file}: готово')

if __name__ == '__main__':
    main()
