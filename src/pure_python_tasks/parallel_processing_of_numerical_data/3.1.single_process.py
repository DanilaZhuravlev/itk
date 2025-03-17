import random
import math
import time
import json

def generate_data(lst,n):
    for i in range(n):
        lst.append(random.randint(1,1000))
    return lst


def process_number(lst):
    return [math.factorial(i) for i in lst]

lst = []

start_time_total = time.time()
result_generate_data = generate_data(lst,100000)
result_process_number = process_number(result_generate_data)
end_time_total= time.time()
execution_time = end_time_total - start_time_total

with open("results_single.json", "w") as f:
    json.dump({
        "execution_time": execution_time
    }, f)


print(f"Общее время выполнения обеих задач: {execution_time:.6f} секунд")

#Общее время выполнения обеих задач: 1.486603 секунд
