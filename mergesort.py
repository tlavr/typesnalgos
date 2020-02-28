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
        if idx1 == idx2 or (idx1 == (idx2 - 1) and arr[idx1] <= arr[idx2]):
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
            if idx1 < n:
                idx1 += 1
            if idx2 > n:
                idx2 -= 1




def kthOrderStatistics(arr, k):
    L = 0
    R = arr.__len__() - 1
    while L != R:
        [L, R] = KthOrderStatisticsStep(arr, L, R, k)


def MergeSort(arr):
    if arr.__len__() <= 1:
        return arr
    n = arr.__len__() // 2
    ar1 = MergeSort(arr[0:n])
    ar2 = MergeSort(arr[n:arr.__len__()])
    ansList = []
    while ar1.__len__() > 0 and ar2.__len__() > 0:
        kthOrderStatistics(ar1, 0)
        kthOrderStatistics(ar2, 0)
        if ar1[0] < ar2[0]:
            ansList.append(ar1.pop(0))
        else:
            ansList.append(ar2.pop(0))
    if ar1.__len__() > 0:
        for el in ar1:
            ansList.append(el)
    elif ar2.__len__() > 0:
        for el in ar2:
            ansList.append(el)
    return ansList





