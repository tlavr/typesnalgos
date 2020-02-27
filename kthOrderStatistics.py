def swap(arr, idx1, idx2):
    tmp = arr[idx2]
    arr[idx2] = arr[idx1]
    arr[idx1] = tmp


def KthOrderStatisticsStep(arr, L = 0, R = None, k = 0):
    if arr.__len__() == 0:
        return None
    if R is None:
        R = arr.__len__() - 1
    idx1 = L
    idx2 = R
    n = (L + R) // 2
    el = arr[n]
    while True:
        while arr[idx1] < el:
            idx1 += 1
        while arr[idx2] > el:
            idx2 -= 1
        if idx1 == (idx2 - 1):
            if arr[idx1] > arr[idx2]:
                swap(arr, idx1, idx2)
                n = (L + R) // 2
                el = arr[n]
                idx1 = L
                idx2 = R
                continue
        elif idx1 == idx2 or (idx1 == (idx2 - 1) and arr[idx1] <= arr[idx2]):
            if n == k:
                return [n, n]
            elif n < k:
                return [n + 1, R]
            else:
                return [L, n-1]
        else:
            swap(arr, idx1, idx2)
            if idx1 == n:
                n = idx2
            elif idx2 == n:
                n = idx1

