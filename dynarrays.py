import ctypes

class DynArray:
    def __init__(self):
        self.count = 0
        self.capacity = 16
        self.array = self.make_array(self.capacity)

    def __len__(self):
        return self.count

    def print_arr(self):
        print('array len: ', self.__len__())
        print('array cap: ', self.capacity)
        print('array: \n')
        if self.count != 0:
            for j in range(self.count):
                print(self.array[j],' ')

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __getitem__(self, i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        return self.array[i]

    def resize(self, new_capacity):
        if new_capacity < 16:
            new_capacity = 16
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, itm):
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        self.array[self.count] = itm
        self.count += 1

    def insert(self, i, itm):
        # добавляем объект itm в позицию i, начиная с 0
        if i < 0 or i > self.count:
            raise IndexError('Index is out of bounds')
        elif i == self.count:
            self.append(itm)
            return
        elif (self.count == self.capacity):
            self.resize(2 * self.capacity)
        for j in range(self.count - i):
            self.array[self.count - j] = self.array[self.count-j-1]
        self.array[i] = itm
        self.count += 1


    def delete(self, i):
        # удаляем объект в позиции i
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        elif (self.count-1 < 0.5*self.capacity and self.capacity > 16):
            self.resize(int(self.capacity / 1.5))
        for j in range(self.count - i - 1):
            self.array[i+j] = self.array[i+j+1]
        self.count -= 1
