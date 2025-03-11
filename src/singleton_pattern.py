# Синглтон с использованием метакласса
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SingletonClass(metaclass=SingletonMeta):
    def __init__(self):
        print("Инициализация объекта")

obj1 = SingletonClass()
obj2 = SingletonClass()

print(obj1 is obj2)

# Синглтон через метод __new__
class SingletonClass:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("Инициализация объекта")

obj1 = SingletonClass()
obj2 = SingletonClass()

print(obj1 is obj2)

# singleton.py
class SingletonClass:
    def __init__(self):
        print("Инициализация объекта")
        self.value = 42


singleton = SingletonClass()  # Создается только один экземпляр

# main.py
import singleton  # Импорт модуля в main.py(как пример) для создания единственного экземпляра класса

obj1 = singleton.SingletonClass()
obj2 = singleton.SingletonClass()

print(obj1 is obj2)