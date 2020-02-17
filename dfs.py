class Vertex:

    def __init__(self, val):
        self.Value = val
        self.Hit = False


class SimpleGraph:

    def __init__(self, size):
        self.max_vertex = size
        self.m_adjacency = [[0] * size for _ in range(size)]
        self.vertex = [None] * size
        self.way = Stack()

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
            ansList.append(self.way.pop())
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
                else:
                    break
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
            else:
                break
        self.way.pop()
        if self.way.size() == 0:
            return []
        return self.DepthFirstSearch(self.way.pop(),VTo,False)


class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
        self.prev = None

class LinkedList2:
    def __init__(self):
        self.head = None
        self.tail = None
    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
            item.prev = None
            item.next = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item
    def add_in_head(self, newNode):
        newNode.next = None
        newNode.prev = None
        if self.head is None:
            self.add_in_tail(newNode)
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
    def delete(self, val, all=False):
        node = self.head
        while node is not None:
            if node.value == val:
                if node.next is not None:
                    if node.prev is None:
                        self.head = node.next
                        self.head.prev = None
                        if all:
                            self.delete(val, True)
                        else:
                            return
                    else:
                        node.next.prev = node.prev
                        node.prev.next = node.next
                        if all:
                            self.delete(val, True)
                        else:
                            return
                else:
                    if node.prev is not None:
                        self.tail = node.prev
                        self.tail.next = None
                        return
                    else:
                        self.head = None
                        self.tail = None
                        return
            node = node.next
    def len(self):
        ans = 0
        node = self.head
        while node is not None:
            ans += 1
            node = node.next
        return ans

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
        return None  # если стек пустой
    def push(self, value):
        self.stack.add_in_head(Node(value))
    def peek(self):
        if self.size() > 0:
            ans = self.stack.head.value
            return ans
        return None  # если стек пустой