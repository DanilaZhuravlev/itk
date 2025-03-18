import redis
import json

def redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)

class RedisQueue:
    def __init__(self, queue_name="default_queue"):
        self.redis_conn = redis_client()
        self.queue_name = queue_name

    def publish(self, msg: dict):
        message_json = json.dumps(msg)
        self.redis_conn.rpush(self.queue_name, message_json)

    def consume(self, timeout=5):  # Добавим параметр таймаута
        result = self.redis_conn.blpop(self.queue_name, timeout=timeout)
        if result:
            queue_name, message_bytes = result
            message_str = message_bytes.decode('utf-8')
            msg = json.loads(message_str)
            return msg
        else:
            return None


if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}

