class BloomFilter:

    def __init__(self, f_len):
        self.filter_len = f_len
        # создаём битовый массив длиной f_len ...
        self.filter = 0

    def hash1(self, str1):
        # 17
        # реализация ...
        hash = 0
        for c in str1:
            code = ord(c)
            hash = (hash * 17 + code) % self.filter_len
        hash = pow(2, hash)
        return hash


    def hash2(self, str1):
        # 223
        hash = 0
        for c in str1:
            code = ord(c)
            hash = (hash * 223 + code) % self.filter_len
        hash = pow(2,hash)
        return hash

    def add(self, str1):
        # добавляем строку str1 в фильтр
        self.filter = self.filter | self.hash1(str1) | self.hash2(str1)

    def is_value(self, str1):
        # проверка, имеется ли строка str1 в фильтре
        hash = self.hash1(str1) | self.hash2(str1)
        isval = self.filter & hash
        if isval == hash:
            return True
        return False