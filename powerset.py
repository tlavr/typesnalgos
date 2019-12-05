# наследуйте этот класс от HashTable
# или расширьте его методами из HashTable
class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, value):
        # в качестве value поступают любые типы!
        # всегда возвращает корректный индекс слота
        # всегда возвращает корректный индекс слота
        hash = 0
        if type(value) == str:
            for i in value:
                hash = (hash*17 + ord(i)) % self.size
        else:
            hash = round(value) % self.size

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

class PowerSet(HashTable):

    def __init__(self):
        self.hash = HashTable(20000,0)
        self.len = 0
        # ваша реализация хранилища

    def size(self):
        return self.len
        # количество элементов в множестве

    def put(self, value):
        # всегда срабатывает
        isput = self.hash.put(value)
        if isput is not None:
            self.len += 1

    def get(self, value):
        # возвращает True если value имеется в множестве,
        # иначе False
        #value = str(value)
        if self.hash.find(value) != None:
            return True
        return False

    def remove(self, value):
        # возвращает True если value удалено
        # иначе False
        #value = str(value)
        idx = self.hash.find(value)
        if idx != None:
            self.hash.slots[idx] = None
            self.len -= 1
            return True
        return False

    def intersection(self, set2):
        # пересечение текущего множества и set2
        if set2 is not None:
            set_inter = PowerSet()
            for item in set2.hash.slots:
                if item != None:
                    if self.get(item):
                        set_inter.put(item)
            if set_inter.size() is 0:
                return None
            return set_inter
        return None

    def union(self, set2):
        # объединение текущего множества и set2
        if set2 is not None:
            set_union = PowerSet()
            for item in set2.hash.slots:
                if item is not None:
                    set_union.put(item)
            for item in self.hash.slots:
                if item is not None:
                    set_union.put(item)
            if set_union.size() is 0:
                return None
            return set_union
        return None

    def difference(self, set2):
        # разница текущего множества и set2
        if set2 is not None:
            set_dif = self.union(set2)
            set_int = self.intersection(set2)
            if set_dif is not None:
                if set_int is not None:
                    for item in set_dif.hash.slots:
                        if item != None:
                            if set_int.get(item):
                                set_dif.remove(item)
                if set_dif.size() is 0:
                    return None
            return set_dif
        return None

    def issubset(self, set2):
        # возвращает True, если set2 есть
        # подмножество текущего множества,
        # иначе False
        if set2 is not None:
            if set2.size() <= self.size():
                if set2.size() == 0:
                    return True
                set_int = self.intersection(set2)
                if set_int is not None:
                    if self.intersection(set2).size() == set2.size():
                        return True
            return False
        return True