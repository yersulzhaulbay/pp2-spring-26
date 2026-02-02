n = int(input())
a = list(map(int,input().split()))
a.sort()
m_f = 1
c_f = 1
result = a[0]
for i in range(1, n):
    if a[i] == a[i - 1]:
        c_f += 1
    else:
        if c_f > m_f:
            m_f = c_f
            result = a[i - 1]
        c_f = 1
if c_f > m_f:
    result = a[-1]
print(result)
