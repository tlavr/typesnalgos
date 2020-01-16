from bBST_func import *
from bBST import *
import random


# функция для печати содержимого листьев
def printAllNodes(nodes,treeName):
    print(treeName)
    for node in nodes:
        tmpNode = BSTNode(None,None)
        tmpNode.NodeKey = node.NodeKey
        tmpNode.LeftChild = node.LeftChild
        tmpNode.RightChild = node.RightChild
        tmpNode.Parent = node.Parent
        tmpNode.Level = node.Level
        if tmpNode.Parent is None:
            tmpNode.Parent = BSTNode(None,None)
        if tmpNode.LeftChild is None:
            tmpNode.LeftChild = BSTNode(None,None)
        if tmpNode.RightChild is None:
            tmpNode.RightChild = BSTNode(None,None)
        print('Node Key: ' + str(tmpNode.NodeKey) + ' Left ChildKey: ' + str(tmpNode.LeftChild.NodeKey)
              + ' Right ChildKey: ' + str(tmpNode.RightChild.NodeKey) + ' Parent NodeKey: '+str(tmpNode.Parent.NodeKey)
              + ' Node Level: ' + str(tmpNode.Level))
    print('\n')

a = [] # not full: 1 element in the left subtree , 1 in the right
b = [] # full
c = [] # with one more level in the left subtree
for ii in range(1,10):
    a.append(ii)
for ii in range(1,16):
    b.append(ii)
    c.append(ii)
c.append(16)
random.shuffle(a)
random.shuffle(b)
random.shuffle(c)
print('a: '+str(a))
print('b: '+str(b))
print('c: '+str(c))

a_out = GenerateBBSTArray(a)
print('a_out :'+str(a_out))
b_out = GenerateBBSTArray(b)
print('b_out :'+str(b_out))
c_out = GenerateBBSTArray(c)
print('c_out :'+str(c_out))

a_tree = BalancedBST()
b_tree = BalancedBST()
c_tree = BalancedBST()

a_tree.GenerateTree(a)
b_tree.GenerateTree(b)
c_tree.GenerateTree(c)

printAllNodes(a_tree.getAllNodes(), 'a tree')
printAllNodes(b_tree.getAllNodes(), 'b tree')
printAllNodes(c_tree.getAllNodes(), 'c tree')

print(a_tree.IsBalanced(a_tree.Root))
print(b_tree.IsBalanced(b_tree.Root))
print(c_tree.IsBalanced(c_tree.Root))