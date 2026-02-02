n = int(input())          
a = list(map(int,input().split()))
max = a[0]
min = a[0]
for i in range(1,n):
    if a[i]>max:
        max = a[i]
    if a[i]<min:
        min = a[i]
for i in range(n):
    if a[i]==max:
       a[i]=min
print(*a)