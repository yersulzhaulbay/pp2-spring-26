n = int(input())          
a = input().split()
cnt = 0
for i in range(n):
    if int(a[i])>0:
        cnt+=1
print(cnt)