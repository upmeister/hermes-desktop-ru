#!/usr/bin/env python3
"""Точечные фиксы en.ts: битый apiKey + 2 запятые."""
import json

path = '/home/covhnw/projects/hermes-agent-dev/apps/desktop/src/i18n/en.ts'
src = open(path, encoding='utf-8').read()

# 1. битый apiKey в settings.mcp
i = src.find("noOutput: 'No output yet.'")
assert i != -1, 'noOutput not found'
j = src.find('apiKey:', i)
assert j != -1, 'apiKey not found'
k = src.find(',', j)
src = src[:i] + "noOutput: 'No output yet.'," + src[i + len("noOutput: 'No output yet.'"):]
# после замены индексы сместились — пересчитаем apiKey
j = src.find('apiKey:', i)
k = src.find(',', j)
src = src[:j] + "apiKey: 'API key'" + src[k:]

# 2. запятая после закрытия appearance.pet перед searchThemes
old2 = "turnOffFailed: 'Could not turn the pet off.'\n      }\n      searchThemes:"
assert src.count(old2) == 1, f'old2: {src.count(old2)}'
src = src.replace(old2, "turnOffFailed: 'Could not turn the pet off.'\n      },\n      searchThemes:")

# 3. запятая после invalidShortcut
old3 = "invalidShortcut: 'Not a valid shortcut. Include at least one modifier key.'\n      currentTarget:"
assert src.count(old3) == 1, f'old3: {src.count(old3)}'
src = src.replace(old3, "invalidShortcut: 'Not a valid shortcut. Include at least one modifier key.',\n      currentTarget:")

open(path, 'w', encoding='utf-8').write(src)
print('en.ts: 3 фикса применены')

# источник: починить apiKey в warment_added_keys.json
k = json.load(open('/home/covhnw/projects/hermes-desktop-ru/warment_added_keys.json'))
k['settings.mcp.apiKey'] = {'en': "'API key'", 'ru': "'API-ключ'", 'translated': True}
json.dump(k, open('/home/covhnw/projects/hermes-desktop-ru/warment_added_keys.json', 'w'), ensure_ascii=False, indent=1)
print('warment_added_keys.json: apiKey исправлен')
