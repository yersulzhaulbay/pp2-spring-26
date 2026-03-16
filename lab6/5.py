s = input()
vowels = "aAeEiIoOuU"

if any(char in vowels for char in s):
    print("Yes")
else:
    print("No")