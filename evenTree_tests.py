from evenTree import *
import time
import unittest

# функция для печати содержимого листьев
def printAllNodes(nodes,treeName):
    print(treeName + ':')
    for node in nodes:
        print('Node Lvl: ' + str(node.lvl) + ' Node Value: '
              + str(node.NodeValue)+' Num of children: ' + str(node.Children.__len__())
              + ' Node Addr: ' + str(node) + ' Parent Node: '+str(node.Parent))
    print('\n')

class testTree(unittest.TestCase):
    def testAll(self):
        # создаем тестовые узлы
        testRootNode = SimpleTreeNode(1,None)
        testChild2 = SimpleTreeNode(2,testRootNode)
        testChild3 = SimpleTreeNode(3,testRootNode)
        testChild6 = SimpleTreeNode(6,testRootNode)
        testChild5 = SimpleTreeNode(5, testChild2)
        testChild7 = SimpleTreeNode(7, testChild2)
        testChild4 = SimpleTreeNode(4, testChild3)
        testChild8 = SimpleTreeNode(8, testChild6)
        testChild9 = SimpleTreeNode(9, testChild8)
        testChild10 = SimpleTreeNode(10, testChild8)

        # создаем деревья и сразу тестируем работу метода
        testTree = SimpleTree(testRootNode) #with children
        testTree.AddChild(testRootNode,testChild2)
        testTree.AddChild(testRootNode, testChild3)
        testTree.AddChild(testRootNode, testChild6)
        testTree.AddChild(testTree.FindNodesByValue(2)[0],testChild5)
        testTree.AddChild(testTree.FindNodesByValue(2)[0], testChild7)
        testTree.AddChild(testTree.FindNodesByValue(3)[0], testChild4)
        testTree.AddChild(testTree.FindNodesByValue(6)[0], testChild8)
        testTree.AddChild(testTree.FindNodesByValue(8)[0], testChild9)
        testTree.AddChild(testTree.FindNodesByValue(8)[0], testChild10)
        printAllNodes(testTree.GetAllNodes(), 'all Nodes')
        printAllNodes(testTree.EvenTrees(), 'delete Nodes')
        self.assertEqual(testTree.EvenTrees(),[testRootNode,testChild3,testRootNode,testChild6],'Even, 1-3,1-6')


unittest.main(verbosity=2)