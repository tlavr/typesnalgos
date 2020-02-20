def swap(arr, idx1, idx2):
    tmp = arr[idx2]
    arr[idx2] = arr[idx1]
    arr[idx1] = tmp


def ArrayChunk(arr):
    n = arr.__len__() // 2
    el = arr[n]
    idx1 = 0
    idx2 = arr.__len__() - 1
    while 1:
        if arr[idx1] < el:
            idx1 += 1
        if arr[idx2] > el:
            idx2 -= 1
        if idx1 == idx2 - 1:
            if arr[idx1] > arr[idx2]:
                swap(arr, idx1, idx2)
                el = arr[n]
                idx1 = 0
                idx2 = arr.__len__() - 1
            else:
                return n
        if idx1 == idx2:
            return n
        swap(arr, idx1, idx2)
        if idx1 == n:
            n = idx2
        else:
            if idx2 == n:
                n = idx1
