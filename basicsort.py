def swap(arr, idx1, idx2):
    tmp = arr[idx2]
    arr[idx2] = arr[idx1]
    arr[idx1] = tmp

def SelectionSortStep(arr, el):
    idx = el
    for ii in range(el, arr.__len__()):
        if arr[ii] < arr[idx]:
            idx = ii
    if idx != el:
        swap(arr,idx,el)

def BubbleSortStep(arr):
    isSwap = False
    for ii in range(arr.__len__()-1):
        if arr[ii] > arr[ii+1]:
            swap(arr,ii,ii+1)
            isSwap = True
    if not isSwap:
        return True
    return False

def InsertionSortStep(arr, step, bidx):
    isOk = False
    while not isOk:
        idx = bidx
        isSwap = False
        while idx + step < arr.__len__():
            if arr[idx] > arr[idx+step]:
                swap(arr,idx,idx+step)
                isSwap = True
            idx = idx + step
        if not isSwap:
            isOk = True