def is_even(x):
    return x % 2 == 0

n = int(input())
numbers = list(map(int, input().split()))

even_n = list(filter(is_even, numbers))
print(len(even_n))