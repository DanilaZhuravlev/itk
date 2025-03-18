import redis
import time
import random

class RateLimitExceed(Exception):
    def __init__(self, message="Rate limit exceeded!"):
        super().__init__(message)

def redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)

class RateLimiter:
    def __init__(self, request_limit=3, window_seconds=5, redis_key_prefix="rate_limit"):
        self.redis_conn = redis_client()
        self.redis_key = f"{redis_key_prefix}:api_requests"
        self.request_limit = request_limit
        self.window_seconds = window_seconds

    def test(self) -> bool:
        current_time = int(time.time())
        window_start_time = current_time - self.window_seconds

        self.redis_conn.zremrangebyscore(self.redis_key, '-inf', window_start_time)
        request_count = self.redis_conn.zcard(self.redis_key)

        print(f"[DEBUG] {current_time}: {request_count} запросов за {self.window_seconds} сек.")

        if request_count < self.request_limit:
            self.redis_conn.zadd(self.redis_key, {current_time: current_time})
            return True
        else:
            return False

def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed()

if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for i in range(50):
        time.sleep(random.uniform(0.5, 1.5))  # Меньший разброс задержек для теста

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print(f"{i+1}: Rate limit exceeded!")
        else:
            print(f"{i+1}: Запрос выполнен")
