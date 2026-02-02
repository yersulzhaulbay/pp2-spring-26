n = int(input())
a = [input().strip() for i in range(n)]
newbie = {}
for i in range(n):
    s = a[i]
    if s not in newbie:
        newbie[s] = i + 1
for s in sorted(newbie):
    print(s, newbie[s])
