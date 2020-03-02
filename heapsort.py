class Heap:
    def __init__(self):
        self.HeapArray = []  # хранит неотрицательные числа-ключи
        self.__size__ = 0
        self.__maxsize__ = 0

    def MakeHeap(self, a =  None, depth = None):
        # создаём массив кучи HeapArray из заданного
        # размер массива выбираем на основе глубины depth
        if a is None:
            a = []
        if a.__len__() == 0:
            return
        if depth is None:
            depth = 0
            while (pow(2,depth+1) - 1) < a.__len__():
                depth += 1
        self.__maxsize__ = pow(2,depth+1) - 1
        for key in a:
            self.Add(key)

    def __swap__(self, idx1, idx2):
        idx1 = int(idx1)
        idx2 = int(idx2)
        if idx1 >= self.__size__ or idx2 >= self.__size__:
            return
        tmpKey = self.HeapArray[idx1]
        self.HeapArray[idx1] = self.HeapArray[idx2]
        self.HeapArray[idx2] = tmpKey

    def __siftDown__(self, fromIdx):
        # seek for the right place of the element
        if fromIdx >= self.__size__ or fromIdx < 0:
            return
        nextIdx = -1
        if 2*fromIdx + 2 < self.__size__:
            if self.HeapArray[2*fromIdx+2] > self.HeapArray[2*fromIdx + 1]:
                nextIdx = 2*fromIdx + 2
            else:
                nextIdx = 2*fromIdx + 1
        elif 2*fromIdx + 1 < self.__size__:
            nextIdx = 2*fromIdx + 1

        if nextIdx > 0:
            if self.HeapArray[fromIdx] < self.HeapArray[nextIdx]:
                self.__swap__(fromIdx, nextIdx)
                self.__siftDown__(nextIdx)
        return

    def GetMax(self):
        # вернуть значение корня и перестроить кучу
        if self.__size__ == 0:
            return -1  # если куча пуста
        ans = self.HeapArray[0] # remember the answer
        if self.__size__ > 1:
            self.HeapArray[0] = self.HeapArray.pop() # put on the top of heap
        else:
            self.HeapArray.pop()
        self.__size__ -= 1
        self.__siftDown__(0)
        return ans

    def Add(self, key):
        # добавляем новый элемент key в кучу и перестраиваем её
        idx = self.__size__
        if idx < self.__maxsize__:
            self.HeapArray.append(key)
            self.__size__ += 1
            parIdx = (idx - 1) / 2
            if parIdx > 0:
                if (parIdx % round(parIdx+0.1)) == parIdx:
                    parIdx = (idx - 2) / 2
            while parIdx >= 0 and key > self.HeapArray[int(parIdx)]:
                self.__swap__(parIdx, idx)
                idx = parIdx
                parIdx = (idx - 1) / 2
                if parIdx > 0:
                    if parIdx % round(parIdx+0.1) == parIdx:
                        parIdx = (idx - 2) / 2
            return True
        else:
            return False  # если куча вся заполнена

class HeapSort:
    def __init__(self, arr = None):
        if arr is None:
            arr = []
        self.HeapObject = Heap()
        self.HeapObject.MakeHeap(arr)
        self.ansList = []

    def GetNextMax(self):
        self.ansList = []
        el = self.HeapObject.GetMax()
        while el != -1:
            self.ansList.insert(0, el)
            el = self.HeapObject.GetMax()
        return self.ansList
