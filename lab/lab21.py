import numpy as np
import time

# 2.1: задать матрицу A размером 1500*1000
A = np.zeros((1500, 1000))

# 2.2: задать матрицу B размером 1000*1500
B = np.zeros((1000, 1500))

# 2.3: реализовать функцию случайного заполнения матрицы А и B целыми числами от 1 до 100
def fill_matrix_randomly(matrix):
    matrix[:] = np.random.randint(1, 101, size=matrix.shape)

fill_matrix_randomly(A)
fill_matrix_randomly(B)

# 2.4: реализовать функцию умножения матрицы А на матрицу B в однопоточной реализации
def matrix_multiply(A, B):
    start_time = time.time()
    C = np.dot(A, B)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time (single thread): {elapsed_time:.4f} seconds")
    return C

C = matrix_multiply(A, B)
