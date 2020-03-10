class BinarySearch:
    def __init__(self, arr):
        self.array = arr
        self.Left = 0
        self.Right = arr.__len__() - 1
        if self.Right < 0:
            self.Right = 0
        self.isFound = False
        self.isEnd = False

    def Step(self, n):
        if self.array.__len__() == 0:
            self.isEnd = True
        if self.isEnd:
            return
        #if self.Left == self.Right:
        #    if self.array[self.Left] == n:
        #        self.isFound = True
        #    self.isEnd = True
        #    return
        cidx = (self.Left + self.Right) // 2
        if self.array[cidx] == n:
            self.isFound = True
            self.isEnd = True
            return
        elif n < self.array[cidx] and self.Right > 0:
            self.Right = cidx - 1
        elif n > self.array[cidx] and self.Left < (self.array.__len__()-1):
            self.Left = cidx + 1
        if self.Left == self.Right:
            if self.array[self.Left] == n:
                self.isFound = True
            self.isEnd = True
            return

    def GetResult(self):
        if self.isFound:
            return 1
        if self.isEnd:
            return -1
        return 0