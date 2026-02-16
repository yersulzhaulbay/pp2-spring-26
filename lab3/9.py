class Circle:
    def __init__(self,radius):
        self.radius = radius
    def area(self):
        return (self.radius**2)* 3.14159
n = int(input())
print(f"{Circle(n).area():.2f}")