n = int(input())
data = [input().split() for i in range(n)]
totals = {}
for s, num in data:
    num = int(num)
    if s in totals:
        totals[s] += num
    else:
        totals[s] = num
for s in sorted(totals):
    print(s, totals[s])
