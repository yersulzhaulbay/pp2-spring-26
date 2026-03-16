n = int(input())
numbers = list(map(int, input().split()))

truthy_cnt = sum(map(bool, numbers))
print(truthy_cnt)