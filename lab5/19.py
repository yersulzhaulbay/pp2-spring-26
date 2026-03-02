import re
s = input()
rule = re.compile(r'\w+')
words = rule.findall(s)
print(len(words))