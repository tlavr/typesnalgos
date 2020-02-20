def swap(arr, idx1, idx2):
    tmp = arr[idx2]
    arr[idx2] = arr[idx1]
    arr[idx1] = tmp


def ArrayChunk(arr, idx1b=0, idx2b=None):
    if arr.__len__() == 0:
        return None
    if idx2b is None:
        idx2b = arr.__len__() - 1
    idx1 = idx1b
    idx2 = idx2b
    n = (idx2b - idx1b + 1) // 2 + idx1b
    el = arr[n]
    isOk = False
    while not isOk:
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
                isOk = True
                return n
        elif idx1 == idx2:
            isOk = True
            return n
        else:
            swap(arr, idx1, idx2)
            if idx1 == n:
                n = idx2
            elif idx2 == n:
                n = idx1


def QuickSort(arr, left=0, right=None):
    if arr.__len__() == 0:
        return None
    if right is None:
        right = arr.__len__() - 1
    if left == right:
        return arr
    n = ArrayChunk(arr, left, right)
    QuickSort(arr, left, n-1)
    QuickSort(arr, n+1, right)