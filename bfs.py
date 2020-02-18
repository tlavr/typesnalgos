class Vertex:

    def __init__(self, val):
        self.Value = val
        self.Hit = False


class SimpleGraph:

    def __init__(self, size):
        self.max_vertex = size
        self.m_adjacency = [[0] * size for _ in range(size)]
        self.vertex = [None] * size
        self.way = None
        self.que = Queue()

    def AddVertex(self, v):
        # ваш код добавления новой вершины
        # с значением value
        # в свободное место массива vertex
        for idx in range(self.vertex.__len__()):
            if self.vertex[idx] is None:
                self.vertex[idx] = Vertex(v)
                break
        # здесь и далее, параметры v -- индекс вершины

    # в списке  vertex
    def RemoveVertex(self, v):
        # ваш код удаления вершины со всеми её рёбрами
        self.vertex[v] = None
        self.m_adjacency[v] = [0] * self.max_vertex
        for line in self.m_adjacency:
            line[v] = 0

    def IsEdge(self, v1, v2):
        # True если есть ребро между вершинами v1 и v2
        if self.m_adjacency[v1][v2] == 1:
            return True
        return False

    def AddEdge(self, v1, v2):
        # добавление ребра между вершинами v1 и v2
        if self.vertex[v1] is not None and self.vertex[v2] is not None:
            self.m_adjacency[v1][v2] = 1
            self.m_adjacency[v2][v1] = 1

    def RemoveEdge(self, v1, v2):
        # удаление ребра между вершинами v1 и v2
        self.m_adjacency[v1][v2] = 0
        self.m_adjacency[v2][v1] = 0

    def __getListFromWayStack__(self):
        ansList = []
        while self.way.size() != 0:
            ansList.append(self.vertex[self.way.pop()])
        ansList.reverse()
        return ansList

    def DepthFirstSearch(self, VFrom, VTo, isFirst = True):
        # узлы задаются позициями в списке vertex
        # возвращается список узлов -- путь из VFrom в VTo
        # или [] если пути нету
        if self.vertex[VFrom] is None or self.vertex[VTo] is None:
            return []
        if isFirst:
            for v in self.vertex:
                if v is not None:
                    v.Hit = False
            self.way = Stack()
        self.vertex[VFrom].Hit = True
        self.way.push(VFrom)
        if self.IsEdge(VFrom,VTo):
            self.way.push(VTo)
            return self.__getListFromWayStack__()
        for ii in range(self.max_vertex):
            if self.vertex[ii] is not None:
                if self.IsEdge(VFrom,ii):
                    if self.vertex[ii].Hit is False:
                        return self.DepthFirstSearch(ii,VTo,False)
        self.way.pop()
        if self.way.size() == 0:
            return []
        return self.DepthFirstSearch(self.way.pop(),VTo,False)

    def BreadthFirstSearch(self, VFrom, VTo, isFirst = True):
        # узлы задаются позициями в списке vertex
        # возвращается список узлов -- путь из VFrom в VTo
        # или [] если пути нету
        if self.vertex[VFrom] is None or self.vertex[VTo] is None:
            return []
        if isFirst:
            for v in self.vertex:
                if v is not None:
                    v.Hit = False
            self.que = Queue()
            self.way = SimpleTree(SimpleTreeNode(VFrom,None))
            self.vertex[VFrom].Hit = True
        if self.IsEdge(VFrom,VTo):
            self.way.AddChild(self.way.FindNodesByValue(VFrom)[0], SimpleTreeNode(VTo, None))
            node = self.way.FindNodesByValue(VTo)[0]
            ansList = []
            while node is not None:
                ansList.append(self.vertex[node.NodeValue])
                node = node.Parent
            ansList.reverse()
            return ansList
        for ii in range(self.max_vertex):
            if self.vertex[ii] is not None:
                if self.IsEdge(VFrom,ii):
                    if self.vertex[ii].Hit is False:
                        self.vertex[ii].Hit = True
                        self.que.enqueue(ii)
                        self.way.AddChild(self.way.FindNodesByValue(VFrom)[0], SimpleTreeNode(ii, None))
        if self.que.size() == 0:
            return []
        return self.BreadthFirstSearch(self.que.dequeue(), VTo, False)


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

class SimpleTreeNode:
    def __init__(self, val, parent):
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.Children = []  # список дочерних узлов
        self.lvl = 0


class SimpleTree:
    def __init__(self, root):
        self.Root = root  # корень, может быть
        self.__allNodes__ = []
        if root is not None:
            self.__setNodeLvl__(root,1)

    def __setNodeLvl__(self,parentNode,lvl):
        parentNode.lvl = lvl
        if parentNode.Children.__len__() != 0:
            for node in parentNode.Children:
                self.__setNodeLvl__(node,lvl+1)

    def AddChild(self, ParentNode, NewChild):
        # ваш код добавления нового дочернего узла существующему ParentNode
        ParentNode.Children.append(NewChild)
        NewChild.Parent = ParentNode
        self.__setNodeLvl__(NewChild,ParentNode.lvl+1)

    def DeleteNode(self, NodeToDelete):
        # ваш код удаления существующего узла NodeToDelete
        if self.Root is NodeToDelete:
            self.Root = None
        else:
            PNode = NodeToDelete.Parent
            PNode.Children.remove(NodeToDelete)
            if NodeToDelete.Children.__len__() != 0:
                for Node in NodeToDelete.Children:
                    Node.Parent = PNode
                    PNode.Children.append(Node)

    def GetAllNodes(self, parentNode = None, isFirst = True):
        # ваш код выдачи всех узлов дерева в определённом порядке
        if isFirst:
            self.__allNodes__ = []
        if parentNode is None:
            parentNode = self.Root
        if parentNode is not None:
            self.__allNodes__.append(parentNode)
            if parentNode.Children.__len__() != 0:
                for node in parentNode.Children:
                    self.GetAllNodes(node, False)
        return self.__allNodes__

    def FindNodesByValue(self, val):
        valNodes = []
        # ваш код поиска узлов по значению
        nodes = self.GetAllNodes()
        for node in nodes:
            if node.NodeValue == val:
                valNodes.append(node)
        return valNodes

    def MoveNode(self, OriginalNode, NewParent):
        # ваш код перемещения узла вместе с его поддеревом --
        # в качестве дочернего для узла NewParent
        OriginalNode.Parent.Children.remove(OriginalNode)
        self.AddChild(NewParent,OriginalNode)

    def Count(self):
        # количество всех узлов в дереве
        return self.GetAllNodes().__len__()

    def LeafCount(self):
        # количество листьев в дереве
        nodes = self.GetAllNodes()
        leavescnt = 0
        for node in nodes:
            if node.Children.__len__() == 0:
                leavescnt += 1
        return leavescnt