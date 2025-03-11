import json
from multiprocessing import Pool, cpu_count
import random
import math
import time

def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]  # Используем твой диапазон

def process_number(data_part):
    return [math.factorial(i) for i in data_part]

if __name__ == "__main__":
    num_processes = cpu_count()
    data_size = 100000

    start_time_total = time.time()

    with Pool(processes=num_processes) as pool:
        data = pool.apply(generate_data, (data_size,))

    chunk_size = data_size // num_processes
    data_chunks = [data[i:i + chunk_size] for i in range(0, data_size, chunk_size)]

    with Pool(processes=num_processes) as pool:
        results_chunks = pool.map(process_number, data_chunks)

    result_process_number = []
    for chunk_result in results_chunks:
        result_process_number.extend(chunk_result)

    end_time_total = time.time()
    execution_time = end_time_total - start_time_total

    with open("results_multiprocessing.Process + multiprocessing.Queue.json", "w") as f:
        json.dump({
            "execution_time": execution_time
        }, f)


    print(f"Общее время выполнения обеих задач (параллельно): {execution_time:.6f} секунд")

#Общее время выполнения обеих задач (параллельно): 1.198704 секунд