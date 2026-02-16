n = int(input())
arr = list(map(int, input().split()))
q = int(input())
for _ in range(q):
    op = input().split()
    cmd = op[0]
    x = int(op[1]) if len(op) > 1 else None

    if cmd == "add":
        arr = [a + x for a in arr]
    elif cmd == "multiply":
        arr = [a * x for a in arr]
    elif cmd == "power":
        arr = [a ** x for a in arr]
    elif cmd == "abs":
        arr = [abs(a) for a in arr]

print(*arr)

