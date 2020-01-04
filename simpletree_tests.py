from simpletree import *
import time

# функция для печати содержимого листьев
def printAllNodes(nodes,treeName):
    print(treeName)
    for node in nodes:
        print('Node Lvl: ' + str(node.lvl) + ' Node Value: '
              + str(node.NodeValue)+' Num of children: ' + str(node.Children.__len__())
              + ' Node Addr: ' + str(node) + ' Parent Node: '+str(node.Parent))
    print('\n')

# создаем тестовые листья
testRootNode = SimpleTreeNode(99,None)
testRootWithChildren = SimpleTreeNode(199,None)
testChild1 = SimpleTreeNode(299,testRootWithChildren)
testChild2 = SimpleTreeNode(298,testRootWithChildren)
testChild3 = SimpleTreeNode(297,testChild1)
testChild1.Children.append(testChild3)
printAllNodes([testRootWithChildren],'No Tree')
testRootWithChildren.Children.append(testChild1)
testRootWithChildren.Children.append(testChild2)

# создаем деревья и сразу тестируем вывод всех узлов
testTree1 = SimpleTree(testRootNode) #without children
testTree2 = SimpleTree(testRootWithChildren) #with children
printAllNodes(testTree1.GetAllNodes(),'1')
printAllNodes(testTree2.GetAllNodes(),'2')

# тестируем поиск узла по значению
Child1 = SimpleTreeNode(299,None)
testTree2.AddChild(testTree2.Root,Child1)
printAllNodes(testTree2.FindNodesByValue(299),'2 Поиск по значению')

# тестируем добавление узла
addNode1 = SimpleTreeNode(98,None)
addNode2 = SimpleTreeNode(97,None)
addNode3 = SimpleTreeNode(96,addNode2)
addNode2.Children.append(addNode3)
testTree1.AddChild(testTree1.Root,addNode1)
testTree1.AddChild(testTree1.Root,addNode2)
printAllNodes(testTree1.GetAllNodes(),'1 Добавление узла')

# тестируем удаление узла
testTree1.DeleteNode(testTree1.FindNodesByValue(96)[0])
printAllNodes(testTree1.GetAllNodes(),'1 Удаление узла')

# тестируем перемещение узла
moveNode1 = SimpleTreeNode(295,None)
testTree2.AddChild(testTree2.FindNodesByValue(299)[0],moveNode1)
printAllNodes(testTree2.GetAllNodes(),'2 Перемещение узла: до')
testTree2.MoveNode(testTree2.FindNodesByValue(299)[0],testTree2.FindNodesByValue(298)[0])
printAllNodes(testTree2.GetAllNodes(),'2 Перемещение узла: после')

# тестируем подсчет количества узлов в дереве
printAllNodes(testTree2.GetAllNodes(),'2 Количество узлов в дереве')
print('2 Количество узлов в дереве: '+str(testTree2.Count())+'\n')
printAllNodes(testTree1.GetAllNodes(),'1 Количество узлов в дереве')
print('1 Количество узлов в дереве: '+str(testTree1.Count())+'\n')

# тестируем подсчет количества листьев в дереве
printAllNodes(testTree2.GetAllNodes(),'2 Количество листьев в дереве')
print('2 Количество листьев в дереве: '+str(testTree2.LeafCount())+'\n')
printAllNodes(testTree1.GetAllNodes(),'1 Количество листьев в дереве')
print('1 Количество листьев в дереве: '+str(testTree1.LeafCount())+'\n')

# тест добавления большого количества эелементов и их вывод
start_time = time.clock()
node1 = SimpleTreeNode(-1,None)
prevNode = node1
testTree1.AddChild(testTree1.Root,node1)
for ii in range(200000):
    newNode = SimpleTreeNode(ii,None)
    testTree1.AddChild(prevNode, newNode)
    if ii % 2 == 0:
        prevNode = newNode

print(time.clock() - start_time, "seconds")

start_time = time.clock()
#printAllNodes(testTree1.GetAllNodes(),'1 Много элементов')
print(time.clock() - start_time, "seconds")