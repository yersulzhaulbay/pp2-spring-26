n = int(input())
nums = []
for i in range(n):
    num = input().strip()
    nums.append(num)
f = {}
for num in nums:
    if num in f:
        f[num] += 1
    else:
        f[num] = 1
cnt = 0
for num in f:
    if f[num] == 3:
        cnt += 1
print(cnt)
