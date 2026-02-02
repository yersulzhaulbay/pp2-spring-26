n, l, r = map(int,input().split())
arr = list(map(int,input().split()))
l -= 1
r -= 1
while l < r:
    arr[r], arr[l] = arr[l], arr[r]
    l+=1
    r-=1
print(*arr)