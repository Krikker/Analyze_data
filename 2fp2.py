from functools import reduce

# Задача 1: Вычисление статистики успеваемости студентов
students = [
    {"name": "Alice", "age": 20, "grades": [85, 90, 88, 92]},
    {"name": "Bob", "age": 22, "grades": [78, 89, 76, 85]},
    {"name": "Charlie", "age": 21, "grades": [92, 95, 88, 94]},
    {"name": "David", "age": 19, "grades": [75, 82, 79, 88]},
    {"name": "Eve", "age": 20, "grades": [90, 92, 94, 87]},
    {"name": "Frank", "age": 22, "grades": [84, 88, 85, 90]},
    {"name": "Grace", "age": 21, "grades": [89, 91, 93, 88]},
    {"name": "Hank", "age": 20, "grades": [76, 80, 78, 85]},
    {"name": "Ivy", "age": 22, "grades": [91, 87, 84, 89]},
    {"name": "Jack", "age": 21, "grades": [85, 88, 90, 91]},
    {"name": "Karen", "age": 19, "grades": [78, 82, 80, 85]},
    {"name": "Liam", "age": 20, "grades": [92, 90, 89, 91]},
    {"name": "Mia", "age": 22, "grades": [85, 89, 87, 92]},
    {"name": "Nina", "age": 21, "grades": [90, 88, 92, 87]},
    {"name": "Oliver", "age": 19, "grades": [84, 87, 85, 89]},
    {"name": "Penny", "age": 20, "grades": [88, 91, 90, 85]},
    {"name": "Quinn", "age": 22, "grades": [89, 88, 87, 90]},
    {"name": "Ryan", "age": 21, "grades": [92, 90, 91, 88]},
    {"name": "Sara", "age": 20, "grades": [85, 88, 91, 92]},
    {"name": "Tom", "age": 22, "grades": [88, 89, 90, 87]},
]

# Фильтрация данных
filtered_by_age = list(filter(lambda student: student["age"] == 20, students))
filtered_by_subjects = list(filter(lambda student: all(grade in student["grades"] for grade in [85, 90]), students))

print("Фильтрация по возрасту:")
for student in filtered_by_age:
    print(f"Имя: {student['name']}, Возраст: {student['age']}")

print("\nФильтрация по предметам:")
for student in filtered_by_subjects:
    print(f"Имя: {student['name']}, Оценки: {student['grades']}")

# Преобразование данных
def calculate_student_average(student):
    if student["grades"]:
        return sum(student["grades"]) / len(student["grades"])
    else:
        return 0

student_averages = list(map(calculate_student_average, students))
overall_average = reduce(lambda x, y: x + y, student_averages) / len(student_averages) if student_averages else 0

print("\nСредний балл для каждого студента:")
for student, avg in zip(students, student_averages):
    print(f"Имя: {student['name']}, Средний балл: {avg:.2f}")

print(f"\nОбщий средний балл по всем студентам = {overall_average:.2f}")

# Агрегация данных
max_average = max(student_averages, default=0)
top_students = list(filter(lambda student: calculate_student_average(student) == max_average, students))

print("\nСтудент(ы) с самым высоким средним баллом:")
for student, avg in zip(top_students, [max_average] * len(top_students)):
    print(f"Имя: {student['name']}, Средний балл: {avg:.2f}")

