import re
s = input()
search = re.findall(r'[A-Z]', s)
print(len(search))