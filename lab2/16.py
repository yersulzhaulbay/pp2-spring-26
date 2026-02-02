n = int(input())
a = list(map(int, input().split()))
newbie = set()
for x in a:
    if x in newbie:
        print("NO")
    else:
        print("YES")
        newbie.add(x)
