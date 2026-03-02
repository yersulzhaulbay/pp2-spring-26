import re
s = input()
rule = r'^[A-Z a-z].*[0-9]$'
if re.match(rule, s):
    print("Yes")
else:
    print("No")