from datetime import datetime

def factorial(n):
    """
    Функция вычисляет факториал числа n
    """
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

# Задаем число, для которого нужно посчитать факториал
n = 150000

# Засекаем время начала выполнения
start_time = datetime.now()

# Вычисляем факториал числа n
result = factorial(n)

# Засекаем время окончания выполнения
end_time = datetime.now()

# Выводим результат и время выполнения
#print(f"Факториал числа {n} равен {result}")
print(f"Время выполнения: {end_time - start_time}")
