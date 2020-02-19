def SelectionSortStep(arr, el):
    idx = el
    for ii in range(el, arr.__len__()):
        if arr[ii] < arr[idx]:
            idx = ii
    if idx != el:
        tmp = arr[idx]
        arr[idx] = arr[el]
        arr[el] = tmp
    return arr

def BubbleSortStep(arr):
    isSwap = False
    for ii in range(arr.__len__()-1):
        if arr[ii] > arr[ii+1]:
            tmp = arr[ii+1]
            arr[ii+1] = arr[ii]
            arr[ii] = tmp
            isSwap = True
    if not isSwap:
        return True
    return False