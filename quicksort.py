def swap(arr, idx1, idx2):
    tmp = arr[idx2]
    arr[idx2] = arr[idx1]
    arr[idx1] = tmp

# разбиение Хоара
def ArrayChunk(arr, idx1b=0, idx2b=None):
    if arr.__len__() == 0:
        return None
    if idx2b is None:
        idx2b = arr.__len__() - 1
    idx1 = idx1b
    idx2 = idx2b
    n = (idx2b - idx1b + 1) // 2 + idx1b
    el = arr[n]
    while True:
        while arr[idx1] < el:
            idx1 += 1
        while arr[idx2] > el:
            idx2 -= 1
        if idx1 == (idx2 - 1):
            if arr[idx1] > arr[idx2]:
                swap(arr, idx1, idx2)
                n = (idx2b - idx1b + 1) // 2 + idx1b
                el = arr[n]
                idx1 = idx1b
                idx2 = idx2b
                continue
            else:
                return n
        elif idx1 == idx2:
            return n
        else:
            swap(arr, idx1, idx2)
            if idx1 == n:
                n = idx2
            elif idx2 == n:
                n = idx1


def QuickSort(arr, left=0, right=None):
    if arr.__len__() == 0:
        return
    if right is None:
        right = arr.__len__() - 1
    if left == right:
        return
    n = ArrayChunk(arr, left, right)
    QuickSort(arr, left, n-1)
    QuickSort(arr, n+1, right)

# разбиение Ломуто
def ArrayChunkForTailOpt(arr, idx1b=0, idx2b=None):
    if arr.__len__() == 0:
        return None
    if idx2b is None:
        idx2b = arr.__len__() - 1
    idx1 = idx1b
    idx2 = idx2b
    n = idx2b #(idx2b - idx1b + 1) // 2 + idx1b
    el = arr[n]
    while True:
        while arr[idx1] < el:
            idx1 += 1
        while arr[idx2] > el:
            idx2 -= 1
        if idx1 == (idx2 - 1):
            if arr[idx1] > arr[idx2]:
                swap(arr, idx1, idx2)
                n = idx2b #(idx2b - idx1b + 1) // 2 + idx1b
                el = arr[n]
                idx1 = idx1b
                idx2 = idx2b
                continue
            else:
                return n
        elif idx1 == idx2:
            return n
        else:
            swap(arr, idx1, idx2)
            if idx1 == n:
                n = idx2
            elif idx2 == n:
                n = idx1

def QuickSortTailOptimization(arr, left=0, right=None):
    if arr.__len__() == 0:
        return
    if right is None:
        right = arr.__len__() - 1
    if left == right:
        return
    n = ArrayChunk(arr, left, right)
    if (n - left) < (right - n):
        while n != right:
            n = ArrayChunk(arr, n + 1, right)
        QuickSortTailOptimization(arr, left, n-1)
    else:
        while n != left:
            n = ArrayChunk(arr, left, n - 1)
        QuickSortTailOptimization(arr, n+1, right)
