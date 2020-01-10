class aBST:
    def __init__(self, depth):
        # правильно рассчитайте размер массива для дерева глубины depth:
        self.tree_size = pow(2,depth+1) - 1
        self.Tree = [None] * self.tree_size  # массив ключей
        self.__len__ = 0

    def FindKeyIndex(self, key):
        # ищем в массиве индекс ключа
        curIdx = 0
        while curIdx < self.tree_size:
            if self.Tree[curIdx] is None:
                return -curIdx
            if key == self.Tree[curIdx]:
                return curIdx
            elif key > self.Tree[curIdx]:
                curIdx = 2*curIdx + 2
            else:
                curIdx = 2*curIdx + 1
        return None  # не найден

    def AddKey(self, key):
        # добавляем ключ в массив
        keyIdx = self.FindKeyIndex(key)
        if keyIdx is not None:
            if keyIdx <= 0:
                if keyIdx == 0:
                    if self.Tree[keyIdx] is not None:
                        return 0
                self.Tree[-keyIdx] = key
                self.__len__ += 1
            return abs(keyIdx)
        return -1
        # индекс добавленного/существующего ключа или -1 если не удалось
