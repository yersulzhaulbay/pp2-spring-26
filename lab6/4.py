n = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

dot_product = sum(a * b for a, b in zip(A, B))
print(dot_product)