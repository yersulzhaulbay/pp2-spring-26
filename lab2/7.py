n = int(input())          
a = list(map(int,input().split()))
max = a[0]
pos = 0
for i in range(1,n):
    if a[i]>max:
        max = a[i]
        pos = i
print(pos+1)