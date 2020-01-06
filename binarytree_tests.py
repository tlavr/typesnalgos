from binarytree import *
import time

# функция для печати содержимого листьев
def printAllNodes(nodes,treeName):
    print(treeName)
    for node in nodes:
        tmpNode.NodeValue = node.NodeValue
        tmpNode.NodeKey = node.NodeKey
        tmpNode.LeftChild = node.LeftChild
        tmpNode.RightChild = node.RightChild
        tmpNode.Parent = node.Parent
        if tmpNode.Parent is None:
            tmpNode.Parent = BSTNode(None,None,None)
        if tmpNode.LeftChild is None:
            tmpNode.LeftChild = BSTNode(None,None,None)
        if tmpNode.RightChild is None:
            tmpNode.RightChild = BSTNode(None,None,None)
        print('Node Key: ' + str(tmpNode.NodeKey) + ' Node Value: '
              + str(tmpNode.NodeValue)+' Left ChildKey: ' + str(tmpNode.LeftChild.NodeKey)
              + ' Right ChildKey: ' + str(tmpNode.RightChild.NodeKey) + ' Parent NodeKey: '+str(tmpNode.Parent.NodeKey))
    print('\n')

# создаем и выводим дерево
testNode1 = BSTNode(28,'root',None)
tmpNode = BSTNode(None,None,None)
testTree = BST(testNode1)
printAllNodes(testTree.getAllNodes(),'1')

# add some nodes tests
addVals = [2,1,3,8,6,5,7,16,15,14,10,13,12,11,18,17,19,21,20]
for val in addVals:
    testTree.AddKeyValue(val,val)
testTree.AddKeyValue(29,29)
testTree.AddKeyValue(31,31)
testTree.AddKeyValue(30,30)
printAllNodes(testTree.getAllNodes(),'add')

# min max count tests
minNode = testTree.FinMinMax(testTree.Root,False)
maxNode = testTree.FinMinMax(testTree.Root,True)
print('min: '+str(minNode.NodeKey))
print('max: '+str(maxNode.NodeKey))
print('count: '+str(testTree.Count()))

# delete node tests
printAllNodes(testTree.getAllNodes(),'before delete')
print('count: '+str(testTree.Count()))
testTree.DeleteNodeByKey(16) # delete the node with both children
testTree.DeleteNodeByKey(1) # delete a leaf
testTree.DeleteNodeByKey(28) # delete the node with one children
printAllNodes(testTree.getAllNodes(),'after delete')
print('count: '+str(testTree.Count()))

testTree2 = BST(None)
testTree2.AddKeyValue(2,2)
testTree2.AddKeyValue(1,2)
testTree2.AddKeyValue(3,2)
testTree2.AddKeyValue(9,2)
testTree2.AddKeyValue(0,2)
testTree2.AddKeyValue(11,2)
printAllNodes(testTree2.getAllNodes(),'2')
#testTree2.DeleteNodeByKey(2)
printAllNodes(testTree2.getAllNodes(),'2')

minNode = testTree2.FinMinMax(testTree2.FindNodeByKey(2).Node,False)
maxNode = testTree2.FinMinMax(testTree2.FindNodeByKey(2).Node,True)
#minNode = testTree2.FinMinMax(None,False)
print('min: '+str(minNode.NodeKey))
print('max: '+str(maxNode.NodeKey))