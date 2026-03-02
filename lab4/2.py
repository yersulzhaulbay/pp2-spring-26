n = int(input())
for i in range(0,n+1,2):
    if i+2<=n:
        print(i, end=",")
    else:
        print(i)