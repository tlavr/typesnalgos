def swap(arr, idx1, idx2):
    tmp = arr[idx2]
    arr[idx2] = arr[idx1]
    arr[idx1] = tmp


def ArrayChunk(arr):
    if arr.__len__() == 0:
        return None
    n = arr.__len__() // 2
    el = arr[n]
    idx1 = 0
    idx2 = arr.__len__() - 1
    isOk = False
    while not isOk:
        while arr[idx1] < el:
            idx1 += 1
        while arr[idx2] > el:
            idx2 -= 1
        if idx1 == (idx2 - 1):
            if arr[idx1] > arr[idx2]:
                swap(arr, idx1, idx2)
                n = arr.__len__() // 2
                el = arr[n]
                idx1 = 0
                idx2 = arr.__len__() - 1
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
