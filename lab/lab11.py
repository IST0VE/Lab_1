import threading
from datetime import datetime

def factorial(n, thread_num, results):
    result = 1
    for i in range(1, n+1):
        if i % 3 == thread_num:
            result *= i
    results[thread_num] = result

# Задаем число, для которого нужно посчитать факториал
n = 8

# Засекаем время начала выполнения
start_time = datetime.now()

# Создаем три потока и список для результатов
threads = []
results = [None] * 3
for i in range(3):
    t = threading.Thread(target=factorial, args=(n, i, results))
    threads.append(t)

# Запускаем потоки
for t in threads:
    t.start()

# Ждем, пока потоки завершатся
for t in threads:
    t.join()

# Вычисляем и выводим результат
result = results[0] * results[1] * results[2]
print(f"Факториал числа {n} равен {result}")

# Засекаем время окончания выполнения
end_time = datetime.now()

# Выводим время выполнения
print(f"Время выполнения: {end_time - start_time}")