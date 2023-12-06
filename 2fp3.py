from functools import reduce

users = [
    {"name": "Alice", "expenses": [100, 50, 75, 200]},
    {"name": "Bob", "expenses": [50, 75, 80, 100]},
    {"name": "Charlie", "expenses": [200, 300, 50, 150]},
    {"name": "David", "expenses": [100, 200, 300, 400]},
    {"name": "Eve", "expenses": [150, 120, 180, 250]},
    {"name": "Frank", "expenses": [50, 75, 100, 125]},
    {"name": "Grace", "expenses": [300, 400, 500, 600]},
    {"name": "Hank", "expenses": [75, 100, 125, 150]},
    {"name": "Ivy", "expenses": [200, 250, 300, 350]},
    {"name": "Jack", "expenses": [100, 200, 300, 400]},
    {"name": "Karen", "expenses": [180, 240, 300, 360]},
    {"name": "Liam", "expenses": [150, 180, 210, 240]},
    {"name": "Mia", "expenses": [80, 100, 120, 140]},
    {"name": "Nina", "expenses": [250, 275, 300, 325]},
    {"name": "Oliver", "expenses": [160, 180, 200, 220]},
    {"name": "Penny", "expenses": [70, 90, 110, 130]},
    {"name": "Quinn", "expenses": [140, 160, 180, 200]},
    {"name": "Ryan", "expenses": [350, 375, 400, 425]},
    {"name": "Sara", "expenses": [120, 140, 160, 180]},
    {"name": "Tom", "expenses": [180, 200, 220, 240]}
]

# Отфильтровать пользователей по заданным критериям.
min_expense_criteria = 200
max_expense_criteria = 400
filtered_users = list(filter(lambda user: min_expense_criteria <= sum(user["expenses"]) <= max_expense_criteria, users))

print("Отфильтрованные пользователи:")
for user in filtered_users:
    print(f"{user['name']} - Общие расходы: {sum(user['expenses'])}")

# Рассчитать общую сумму расходов для каждого пользователя.
def calculate_total_expenses(user):
    user["total_expenses"] = sum(user["expenses"])
    return user

users_with_total_expenses = list(map(calculate_total_expenses, users))

print("Общая сумма расходов для каждого пользователя:")
for user in users_with_total_expenses:
    print(f"{user['name']} - Общие расходы: {user['total_expenses']}")

# Получить общую сумму расходов всех пользователей.
total_expenses_all_users = sum(user["total_expenses"] for user in users_with_total_expenses)

print("\nОбщая сумма расходов всех пользователей:", total_expenses_all_users)

# Получить общую сумму расходов всех отфильтрованных пользователей.
total_expenses_all_users = reduce(lambda x, y: x + y, [user["total_expenses"] for user in filtered_users], 0)

print("\nОбщая сумма расходов всех отфильтрованных пользователей:", total_expenses_all_users)
