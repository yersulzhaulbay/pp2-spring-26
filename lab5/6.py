import re
s = input()
email = r'\S+@\S+\.\S+'
match = re.search(email, s)
if match:
    print(match.group())
else:
    print("No email")