n = int(input())
surnames = [input().strip().lower() for i in range(n)]
u_surnames = set(surnames)
print(len(u_surnames))
