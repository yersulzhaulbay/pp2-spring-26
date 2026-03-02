import re
s = input()
rule = re.compile(r'^\d+$')
if rule.fullmatch(s):
    print("Match")
else:
    print("No match")