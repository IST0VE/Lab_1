import numpy as np
import threading
import time

A = np.zeros((1500, 1000))
B = np.zeros((1000, 1500))

def fill_matrix(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i,j] = np.random.randint(1,101)

def matrix_multiply(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(B.shape[0]):
                C[i,j] += A[i,k] * B[k,j]
    return C

def threaded_multiply(A, B, nhor, nvert):
    C = np.zeros((A.shape[0], B.shape[1]))
    threads = []
    for i in range(nhor):
        for j in range(nvert):
            thread = threading.Thread(target=threaded_multiply_helper, args=(A,B,C,i,j))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()
    return C

def threaded_multiply_helper(A, B, C, i, j):
    for k in range(A.shape[1]):
        C[i,j] += A[i,k] * B[k,j]

# заполнение матриц
fill_matrix(A)
fill_matrix(B)

# однопоточное умножение
start_time = time.time()
matrix_multiply(A, B)
end_time = time.time()
single_thread_time = end_time - start_time

# многопоточное умножение
start_time = time.time()
threaded_multiply(A, B, 2, 2)
end_time = time.time()
multi_thread_time = end_time - start_time

print("Время однопоточного умножения: %.2f секунд" % single_thread_time)
print("Время многопоточного умножения: %.2f секунд" % multi_thread_time)
print("Относительное время работы: %.2f%%" % (multi_thread_time / single_thread_time * 100))
