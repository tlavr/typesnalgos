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
        isChanged = True #False
        cidx = (self.Left + self.Right) // 2
        if self.array[cidx] == n:
            self.isFound = True
            self.isEnd = True
            return
        elif n < self.array[cidx] and self.Right > 0:
            self.Right = cidx - 1
            isChanged = True
        elif n > self.array[cidx] and self.Left < (self.array.__len__()-1):
            self.Left = cidx + 1
            isChanged = True
        if self.Left == self.Right - 1:
            if (n < self.array[self.Right] and n > self.array[self.Left]) or n > self.array[self.Right] or n < self.array[self.Left]:
                self.isEnd = True
                return
        if self.Left == self.Right:
            if self.array[self.Left] == n:
                self.isFound = True
            self.isEnd = True
            return
        if not isChanged:
            self.isEnd = True

    def GetResult(self):
        if self.isFound:
            return 1
        if self.isEnd:
            return -1
        return 0


def getIdx(ii):
    return pow(2, ii) - 2


def GallopingSearch(arr, n):
    if arr.__len__() == 0:
        return False
    ii = 1
    curIdx = 0
    while curIdx < arr.__len__() - 1:
        if arr[curIdx] == n:
            return True
        elif arr[curIdx] < n:
            ii += 1
            curIdx = getIdx(ii)
        else:
            break
    if curIdx > arr.__len__() - 1:
        curIdx = arr.__len__() - 1
    bs = BinarySearch(arr)
    bs.Left = getIdx(ii-1) + 1
    bs.Right = curIdx
    while bs.GetResult() == 0:
        bs.Step(n)
    if bs.GetResult() == 1:
        return True
    return False
