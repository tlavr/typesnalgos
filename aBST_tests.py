from aBST import *

def printTree(testTree):
    print('Tree: ' + str(testTree.Tree) + ' ; Num of elements: ' + str(testTree.__len__))

depth = 3
testTree = aBST(depth)
printTree(testTree)
print(testTree.FindKeyIndex(0))

#for ii in range(testTree.tree_size):
#    testTree.AddKey(ii*pow(-1,ii))
keys = [50,25,15,7,18,37,31,43,75,62,84,55,65,81,92]
for key in keys:
    testTree.AddKey(key)
printTree(testTree)
print(testTree.AddKey(4))
print(testTree.FindKeyIndex(0))
