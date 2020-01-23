class Heap:
    def __init__(self):
        self.HeapArray = []  # хранит неотрицательные числа-ключи
        self.__size__ = 0

    def MakeHeap(self, a, depth):
        # создаём массив кучи HeapArray из заданного
        # размер массива выбираем на основе глубины depth
        if a.__len__() == 0:
            return
        arSize = pow(2,depth+1) - 1
        self.HeapArray = [None]*arSize
        #a.sort(reverse=True)
        for key in a:
            self.Add(key)

    def __swap__(self, idx1, idx2):
        idx1 = int(idx1)
        idx2 = int(idx2)
        tmpKey = self.HeapArray[idx1]
        self.HeapArray[idx1] = self.HeapArray[idx2]
        self.HeapArray[idx2] = tmpKey

    def __siftDown__(self, fromIdx):
        # seek for the right place of the element
        if 2*fromIdx + 2 >= self.HeapArray.__len__() or fromIdx < 0 or \
                self.HeapArray[2*fromIdx + 1] is None or self.HeapArray[2*fromIdx + 2] is None:
            return
        if self.HeapArray[fromIdx] < self.HeapArray[2*fromIdx + 1]:
            self.__swap__(fromIdx,2*fromIdx+1)
            self.__siftDown__(2*fromIdx+1)
            self.__siftDown__(fromIdx)
        if self.HeapArray[fromIdx] < self.HeapArray[2*fromIdx + 2]:
            self.__swap__(fromIdx,2*fromIdx+2)
            self.__siftDown__(2*fromIdx+2)
            self.__siftDown__(fromIdx)
        return

    def GetMax(self):
        # вернуть значение корня и перестроить кучу
        if self.__size__ == 0:
            return -1  # если куча пуста
        ans = self.HeapArray[0] # remember the answer
        curIdx = 0 #to find the last meaning value in the array
        for idx in range(self.HeapArray.__len__()-1):
            if self.HeapArray[idx+1] is None:
                break
            curIdx = idx+1
        self.HeapArray[0] = self.HeapArray[curIdx] # put on the top of heap
        self.HeapArray[curIdx] = None
        self.__size__ -= 1
        self.__siftDown__(0)
        return ans

    def Add(self, key):
        # добавляем новый элемент key в кучу и перестраиваем её
        idx = 0
        for el in self.HeapArray:
            if self.HeapArray[idx] is None:
                break
            idx += 1
        if idx < self.HeapArray.__len__():
            self.HeapArray[idx] = key
            parIdx = (idx - 1) / 2
            if parIdx > 0:
                if (parIdx % round(parIdx+0.1)) == parIdx:
                    parIdx = (idx - 2) / 2
            while parIdx >= 0 and key > self.HeapArray[int(parIdx)]:
                self.__swap__(int(parIdx), int(idx))
                idx = parIdx
                parIdx = (idx - 1) / 2
                if parIdx > 0:
                    if parIdx % round(parIdx+0.1) == parIdx:
                        parIdx = (idx - 2) / 2
            self.__size__ += 1
            return True
        else:
            return False  # если куча вся заполнена
