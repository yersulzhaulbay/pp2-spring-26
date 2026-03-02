import re
s = input()
search = re.findall(r'\b\w{3}\b', s)
print(len(search))