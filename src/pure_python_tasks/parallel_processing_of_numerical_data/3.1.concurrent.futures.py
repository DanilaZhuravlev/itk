import json
from concurrent.futures import ThreadPoolExecutor
import random
import math
import time

def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]

def process_number(lst):
    return [math.factorial(i) for i in lst]

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        start_time_total = time.time()

        future_generate_data = executor.submit(generate_data, 100000)
        data = future_generate_data.result()

        future_process_data = executor.submit(process_number, data)
        processed_data = future_process_data.result()

        end_time_total = time.time()
        execution_time = end_time_total - start_time_total

        with open("results_concurrent.json", "w") as f:
            json.dump({
                "execution_time": execution_time
            }, f)

        print(f"Общее время выполнения обеих задач (параллельно): {execution_time:.6f} секунд")

#Общее время выполнения обеих задач (параллельно): 1.484213 секунд