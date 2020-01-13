def makeAr(leftHalf,rightHalf, outList,curIdx):
    if leftHalf.__len__() > 0:
        centIdx = round(leftHalf.__len__()/2 - 0.1)
        outList[2 * curIdx + 1] = leftHalf[centIdx]
        if centIdx != 0:
            makeAr(leftHalf[:centIdx], leftHalf[centIdx + 1:], outList, 2 * curIdx + 1)
    if rightHalf.__len__() > 0:
        centIdx = round(rightHalf.__len__() / 2 - 0.1)
        outList[2 * curIdx + 2] = rightHalf[centIdx]
        if centIdx != 0:
            makeAr(rightHalf[:centIdx], rightHalf[centIdx + 1:], outList, 2 * curIdx + 2)

def GenerateBBSTArray(a):
    # Determine tree depth
    if a.__len__() == 0:
        return None
    h = 1 # tree array size
    h_i = 0 # tree depth
    while h < a.__len__():
        h = pow(2,h_i+1)-1
        h_i += 1
    outList = [None]*h
    # Sort array
    a = sorted(a)
    # Recursive add all elements
    makeAr([], a, outList, -1) # parameters for the first adding
    # output
    return outList
