import functools
import datetime
import redis
import time
import threading

def redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)

def single(max_processing_time: datetime.timedelta):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            redis_conn = redis_client()
            lock_key = f"lock:{func.__module__}.{func.__name__}"
            lock_timeout_seconds = int(max_processing_time.total_seconds())
            thread_name = threading.current_thread().name

            print(f"Поток {thread_name}: Попытка захвата лока для {func.__name__}")

            lock_acquired = redis_conn.setnx(lock_key, "locked")
            if lock_acquired:
                redis_conn.expire(lock_key, lock_timeout_seconds)
                print(f"Поток {thread_name}: Лок успешно захвачен для {func.__name__}")
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    redis_conn.delete(lock_key)
                    print(f"Поток {thread_name}: Лок освобожден для {func.__name__}")
            else:
                print(f"Поток {thread_name}: Лок уже занят для {func.__name__}. Пропускаем выполнение.")
                return None
        return wrapper
    return decorator

@single(max_processing_time=datetime.timedelta(seconds=5))
def process_task():
    """
    Имитация задачи, которая должна выполняться не параллельно.
    """
    task_id = threading.current_thread().name
    print(f"Задача {task_id}: Начало выполнения process_task")
    time.sleep(2)
    print(f"Задача {task_id}: Завершение выполнения process_task")

if __name__ == "__main__":
    client = redis_client()
    try:
        response = client.ping()
        if response:
            print("Успешно подключились к Redis!")
        else:
            print("Не удалось подключиться к Redis.")
    except redis.exceptions.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")

    threads = []
    for i in range(3):
        thread = threading.Thread(target=process_task, name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Все потоки завершили работу.")