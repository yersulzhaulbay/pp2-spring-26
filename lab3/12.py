class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary
    def total_salary(self):
        return self.base_salary
class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent
    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)
class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects
    def total_salary(self):
        return self.base_salary + self.completed_projects * 500
class Intern(Employee):
    pass

data = input().split()
role, name, *args = data
classes = {
    "Manager": Manager,
    "Developer": Developer,
    "Intern": Intern
}
args = list(map(int, args))
employee = classes[role](name, *args)
print(f"Name: {employee.name}, Total: {employee.total_salary():.2f}")
