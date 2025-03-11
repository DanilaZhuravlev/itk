from datetime import datetime

class AutoTimestampMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=AutoTimestampMeta):
    def __init__(self, name):
        self.name = name

# Пример использования
obj1 = MyClass('Object 1')
obj2 = MyClass('Object 2')

print(obj1.created_at)
print(obj2.created_at)
