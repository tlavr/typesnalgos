class NativeDictionary:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size

    def hash_fun(self, key):
        # в качестве key поступают строки!
        # всегда возвращает корректный индекс слота
        hash = 0
        for i in key:
            hash = (hash * 17 + ord(i)) % self.size
        return hash  # hash [0..self.size - 1]

    def is_key(self, key):
        # возвращает True если ключ имеется,
        # иначе False
        idx = self.hash_fun(key)
        if self.slots[idx] is key:
           return True
        return False

    def put(self, key, value):
        idx = self.hash_fun(key)
        self.slots[idx] = key
        self.values[idx] = value
        # гарантированно записываем
        # значение value по ключу key

    def get(self, key):
        # возвращает value для key,
        # или None если ключ не найден
        if self.is_key(key):
            idx = self.hash_fun(key)
            return self.values[idx]
        return None