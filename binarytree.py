class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
        self.prev = None


class LinkedList2:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
            item.prev = None
            item.next = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item
        self.length  += 1

    def add_in_head(self, newNode):
        newNode.next = None
        newNode.prev = None
        if self.head is None:
            self.add_in_tail(newNode)
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
            self.length  += 1

    def delete(self, val, all=False):
        node = self.head
        while node is not None:
            if node.value == val:
                if node.next is not None:
                    if node.prev is None:
                        self.head = node.next
                        self.head.prev = None
                        self.length  -= 1
                        if all:
                            self.delete(val, True)
                        else:
                            return
                    else:
                        node.next.prev = node.prev
                        node.prev.next = node.next
                        self.length  -= 1
                        if all:
                            self.delete(val, True)
                        else:
                            return
                else:
                    if node.prev is not None:
                        self.tail = node.prev
                        self.tail.next = None
                        self.length  -= 1
                        return
                    else:
                        self.head = None
                        self.tail = None
                        self.length  -= 1
                        return
            node = node.next

    def len(self):
        return self.length

class Stack:
    def __init__(self):
        self.stack = LinkedList2()

    def size(self):
        return self.stack.len()

    def pop(self):
        if self.size() > 0:
            ans = self.stack.head.value
            self.stack.delete(ans)
            return ans
        return None # если стек пустой

    def push(self, value):
        self.stack.add_in_head(Node(value))

class Queue:
    def __init__(self):
        self.queue = LinkedList2()

    def enqueue(self, item):
        self.queue.add_in_tail(Node(item))

    def dequeue(self):
        if self.size() > 0:
            ans = self.queue.head.value
            self.queue.delete(ans)
            return ans
        return None # если очередь пустая

    def cycleshift(self,N,left=False):
        # N > 0 - вправо
        # N < 0 - влево
        if N < 0:
            left = True
            N = -N
        if self.size() > 0:
            self.queue.tail.next = self.queue.head
            self.queue.head.prev = self.queue.tail
            node = self.queue.head
            for i in range(N):
                if left:
                    node = node.next
                else:
                    node = node.prev
            self.queue.head = node
            self.queue.tail = node.prev
            self.queue.head.prev = None
            self.queue.tail.next = None

    def size(self):
        return self.queue.len()

class QueueStack:
    def __init__(self):
        self.enq = Stack()
        self.deq = Stack()

    def enqueue(self, item):
        while self.deq.size() > 0:
            self.enq.push(self.deq.pop())
        self.enq.push(item)

    def dequeue(self):
        while self.enq.size() > 0:
            self.deq.push(self.enq.pop())
        return self.deq.pop()

    def size(self):
        return self.enq.size()+self.deq.size()

def cycshift(qu,N):
    for i in range(N):
        qu.enqueue(qu.dequeue())

class BSTNode:
    def __init__(self, key, val, parent):
        self.NodeKey = key  # ключ узла
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.LeftChild = None  # левый потомок
        self.RightChild = None  # правый потомок


class BSTFind:  # промежуточный результат поиска
    def __init__(self):
        self.Node = None  # None если
        # в дереве вообще нету узлов
        self.NodeHasKey = False  # True если узел найден
        self.ToLeft = False  # True, если родительскому узлу надо
        # добавить новый узел левым потомком


class BST:
    def __init__(self, node):
        self.Root = node  # корень дерева, или None
        self.allNodes = []
        if node is not None:
            self.__len__ = 1
        else:
            self.__len__ = 0

    def FindNodeByKey(self, key):
        # ищем в дереве узел и сопутствующую информацию по ключу
        curNode = self.Root
        foundNode = BSTFind()
        while curNode is not None:
            if key == curNode.NodeKey:
                foundNode.Node = curNode
                foundNode.NodeHasKey = True
                curNode = None
            elif key > curNode.NodeKey:
                if curNode.RightChild is not None:
                    curNode = curNode.RightChild
                else:
                    foundNode.Node = curNode
                    curNode = None
            else:
                if curNode.LeftChild is not None:
                    curNode = curNode.LeftChild
                else:
                    foundNode.Node = curNode
                    foundNode.ToLeft = True
                    curNode = None
        return foundNode # возвращает BSTFind

    def AddKeyValue(self, key, val):
        # добавляем ключ-значение в дерево
        addNode = BSTNode(key,val,None)
        foundNode = self.FindNodeByKey(key)
        if foundNode.Node is None:
            self.Root = addNode
            self.__len__ += 1
        elif foundNode.NodeHasKey == True:
            return False  # если ключ уже есть
        else:
            addNode.Parent = foundNode.Node
            if foundNode.ToLeft == True:
                foundNode.Node.LeftChild = addNode
            else:
                foundNode.Node.RightChild = addNode
            self.__len__ += 1
            return True

    def FinMinMax(self, FromNode, FindMax):
        # ищем максимальное/минимальное (узел) в поддереве
        #foundNode = None #BSTNode(None,None,None)
        if FromNode is not None:
            if FindMax == False:
                if FromNode.LeftChild is not None:
                    return self.FinMinMax(FromNode.LeftChild, FindMax)
            else:
                if FromNode.RightChild is not None:
                    return self.FinMinMax(FromNode.RightChild, FindMax)
        return FromNode

    def __isLeaf__(self,node): # 0 -> Leaf, 1 -> has only LeftChild, 2 -> has only RightChild, 3 -> both
        if node.LeftChild is None and node.RightChild is None:
            return 0
        elif node.RightChild is None:
            return 1
        elif node.LeftChild is None:
            return 2
        else:
            return 3

    def __isLeftChild__(self,parentNode,node):
        # determine left or right child
        if parentNode.LeftChild is node:
            return True
        elif parentNode.RightChild is node:
            return False
        else:
            return None

    def DeleteNodeByKey(self, key,out = True):
        # удаляем узел по ключу
        nodeToDel = self.FindNodeByKey(key)
        if nodeToDel.Node is None or nodeToDel.NodeHasKey is False:
            return False  # если узел не найден
        else:
            nodeToDel = nodeToDel.Node
            cond = self.__isLeaf__(nodeToDel)
            if cond == 0: # if node is a leaf
                tmpNode = None
            elif cond == 1: # if node has one left child
                tmpNode = nodeToDel.LeftChild
            elif cond == 2: # if node has one right child
                tmpNode = nodeToDel.RightChild
            else: # if node has both children
                minNode = self.FinMinMax(nodeToDel.RightChild,False) # find the most left node on the right side
                tmpBool = self.DeleteNodeByKey(minNode.NodeKey,False)
                minNode.RightChild = nodeToDel.RightChild
                minNode.LeftChild = nodeToDel.LeftChild
                tmpNode = minNode
            if nodeToDel is self.Root:
                self.Root = tmpNode
                if tmpNode is not None:
                    self.Root.Parent = None
            else:
                if self.__isLeftChild__(nodeToDel.Parent, nodeToDel):
                    nodeToDel.Parent.LeftChild = tmpNode
                else:
                    nodeToDel.Parent.RightChild = tmpNode
                if tmpNode is not None:
                    tmpNode.Parent = nodeToDel.Parent
            if out is True:
                self.__len__ -= 1
            return True

    def __collectAllNodes__(self,fromNode = None, mode = 0):
        if fromNode is None or fromNode is self.Root:
            fromNode = self.Root
            self.allNodes = []
        if fromNode is None:
            return
        if mode == 2:
            self.allNodes.append(fromNode)
        if fromNode.LeftChild is not None:
            self.__collectAllNodes__(fromNode.LeftChild)
        if mode == 0:
            self.allNodes.append(fromNode)
        if fromNode.RightChild is not None:
            self.__collectAllNodes__(fromNode.RightChild)
        if mode == 1:
            self.allNodes.append(fromNode)

    def getAllNodes(self):
        self.__collectAllNodes__()
        return self.allNodes

    def Count(self):
        return self.__len__  # количество узлов в дереве

    # поиск в ширину
    def WideAllNodes(self,fromNode = None, nodes = [], nodeQueue = Queue()):
        if fromNode is None:
            fromNode = self.Root
        if fromNode is None:
            return ()
        nodes.append(fromNode)
        if nodeQueue.size() != 0 or fromNode is self.Root:
            if fromNode.LeftChild is not None:
                nodeQueue.enqueue(fromNode.LeftChild)
            if fromNode.RightChild is not None:
                nodeQueue.enqueue(fromNode.RightChild)
            return self.WideAllNodes(nodeQueue.dequeue(),nodes,nodeQueue)
        else:
            return tuple(nodes)


    # поиск в глубину: 0 - in order, 1 - post order, 2 - pre order
    def DeepAllNodes(self,mode = 0,fromNode = None,nodes = []):
        if fromNode is None:
            fromNode = self.Root
            nodes = []
        if fromNode is None:
            return ()
        if mode == 2:
            nodes.append(fromNode)
        if fromNode.LeftChild is not None:
            self.DeepAllNodes(mode,fromNode.LeftChild,nodes)
        if mode == 0:
            nodes.append(fromNode)
        if fromNode.RightChild is not None:
            self.DeepAllNodes(mode,fromNode.RightChild,nodes)
        if mode == 1:
            nodes.append(fromNode)
        return tuple(nodes)