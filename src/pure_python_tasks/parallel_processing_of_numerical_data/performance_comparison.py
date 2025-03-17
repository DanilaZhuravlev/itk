import json
from tabulate import tabulate


execution_times = {}

variants = [
    {"name": "SingleProcess", "filename": "results_single.json"},
    {"name": "ThreadPoolExecutor", "filename": "results_concurrent.json"},
    {"name": "ProcessPoolExecutor (multiprocessing.Pool)", "filename": "results_multiprocessing.Pool.json"},
    {"name": "ProcessPoolExecutor (multiprocessing.Process + multiprocessing.Queue)", "filename": "results_multiprocessing.Process + multiprocessing.Queue.json"}, # Исправьте имя файла, если оно отличается
]

for variant in variants:
    try:
        with open(variant["filename"], 'r') as f:
            data = json.load(f)
            execution_times[variant["name"]] = data["execution_time"]
    except FileNotFoundError:
        execution_times[variant["name"]] = "Файл не найден"

table_data = []
headers = ["Вариант кода", "Время выполнения (секунд)"]

for variant in variants:
    table_data.append([variant["name"], execution_times[variant["name"]]])

table = tabulate(table_data, headers=headers, tablefmt="grid")
print("Таблица сравнения производительности:")
print(table)
print("\n")