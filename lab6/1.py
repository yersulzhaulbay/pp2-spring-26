def square(x):
    return x * x

n = int(input())
numbers = list(map(int, input().split()))

squares = map(square, numbers)
print(sum(squares))