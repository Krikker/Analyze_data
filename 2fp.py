from functools import reduce

orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150.0},
    {"order_id": 2, "customer_id": 102, "amount": 200.0},
    {"order_id": 3, "customer_id": 101, "amount": 75.0},
    {"order_id": 4, "customer_id": 103, "amount": 100.0},
    {"order_id": 5, "customer_id": 101, "amount": 50.0},
    {"order_id": 6, "customer_id": 102, "amount": 220.0},
    {"order_id": 7, "customer_id": 101, "amount": 85.0},
    {"order_id": 8, "customer_id": 104, "amount": 120.0},
    {"order_id": 9, "customer_id": 101, "amount": 45.0},
    {"order_id": 10, "customer_id": 102, "amount": 180.0},
    {"order_id": 11, "customer_id": 101, "amount": 95.0},
    {"order_id": 12, "customer_id": 105, "amount": 110.0},
    {"order_id": 13, "customer_id": 101, "amount": 55.0},
    {"order_id": 14, "customer_id": 102, "amount": 240.0},
    {"order_id": 15, "customer_id": 101, "amount": 65.0},
    {"order_id": 16, "customer_id": 106, "amount": 130.0},
    {"order_id": 17, "customer_id": 101, "amount": 75.0},
    {"order_id": 18, "customer_id": 102, "amount": 260.0},
    {"order_id": 19, "customer_id": 101, "amount": 105.0},
    {"order_id": 20, "customer_id": 107, "amount": 90.0},
]

# Фильтрация заказов для определенного клиента с заданным идентификатором клиента.
customer_id_to_filter = 101
filtered_orders = list(filter(lambda order: order["customer_id"] == customer_id_to_filter, orders))

print("Отфильтрованные заказы для клиента", customer_id_to_filter)
for order in filtered_orders:
    print(f"Заказ {order['order_id']}, Сумма: {order['amount']}")

# Подсчет общей суммы заказов для данного клиента.
total_amount = reduce(lambda x, y: x + y, map(lambda order: order["amount"], filtered_orders), 0)

print("\nОбщая сумма заказов для клиента", customer_id_to_filter, "составляет", total_amount)

# Подсчет средней стоимости заказов для данного клиента.
if filtered_orders:
    average_amount = total_amount / len(filtered_orders)
else:
    average_amount = 0

print("Средняя стоимость заказов для клиента", customer_id_to_filter, "составляет", average_amount)

