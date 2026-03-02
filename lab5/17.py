import re
s = input()
rule = r'\b\d{2}/\d{2}/\d{4}\b'
matches = re.findall(rule, s)
print(len(matches))