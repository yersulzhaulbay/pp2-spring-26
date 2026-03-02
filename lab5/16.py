import re
s = input()
match = re.match(r'Name:\s*(.+),\s*Age:\s*(.+)', s)
if match:
    name, age = match.groups()
    print(name, age)