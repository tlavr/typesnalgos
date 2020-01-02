class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, value):
        # в качестве value поступают строки!
        # всегда возвращает корректный индекс слота
        # всегда возвращает корректный индекс слота
        hash = 0
        for i in value:
            hash = (hash*17 + ord(i)) % self.size
        return hash # hash [0..self.size - 1]

    def seek_slot(self, value):
        # находит индекс пустого слота для значения, или None
        idx = self.hash_fun(value)
        idx0 = idx
        while self.slots[idx] != None:
            idx = (idx + self.step) % self.size
            if idx == idx0:
                return None
        return idx

    def put(self, value):
        # записываем значение по хэш-функции
        idx = self.seek_slot(value)
        if idx is None:
            return None
        else:
            self.slots[idx] = value
            return idx
        # возвращается индекс слота или None,
        # если из-за коллизий элемент не удаётся
        # разместить

    def find(self, value):
        # находит индекс слота со значением, или None
        idx = self.hash_fun(value)
        idx0 = idx
        while self.slots[idx] != value:
            idx = (idx + self.step) % self.size
            if idx == idx0:
                return None
        return idx

class NativeCache(HashTable):
    def __init__(self, sz):
        super().__init__(sz, 1)
        self.hits = [0] * self.size

    def find(self, value):
        value = str(value)
        idx = super().find(value)
        if idx is not None:
            self.hits[idx] += 1

    def seek_slot(self, value):
        # находит индекс пустого слота для значения, или None
        idx = super().hash_fun(value)
        idx0 = idx
        minhit = idx
        while self.slots[idx] != None:
            idx = (idx + self.step) % self.size
            if self.hits[idx] < self.hits[minhit]:
                minhit = idx
            if idx == idx0:
                return minhit
        return idx

    def put(self, value):
        value = str(value)
        # записываем значение по хэш-функции
        idx = self.seek_slot(value)
        self.slots[idx] = value
        self.hits[idx] = 0
        return idx
        # возвращается индекс слота или None,
        # если из-за коллизий элемент не удаётся
        # разместить


