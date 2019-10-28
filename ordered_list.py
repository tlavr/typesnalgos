class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class OrderedList:
    def __init__(self, asc):
        self.head = None
        self.tail = None
        self.__ascending = asc
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
        self.length += 1

    def add_in_head(self, newNode):
        newNode.next = None
        newNode.prev = None
        if self.head is None:
            self.add_in_tail(newNode)
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
            self.length += 1

    def compare(self, v1, v2):
        if v1.value > v2.value:
            return 1
        elif v1.value < v2.value:
            return -1
        return 0
        # -1 если v1 < v2
        # 0 если v1 == v2
        # +1 если v1 > v2

    def add(self, value):
        newNode = Node(value)
        newNode.next = None
        newNode.prev = None
        node = self.head
        if node is None:
            self.add_in_tail(newNode)
            return
        if self.compare(newNode, node) * (2*self.__ascending - 1) < 0:
            self.add_in_head(newNode)
            return
        while node is not None:
            if self.compare(newNode,node)*(2*self.__ascending - 1) >= 0:
                if node.next is None:
                    self.add_in_tail(newNode)
                    return
                else:
                    if self.compare(newNode, node.next) * (2*self.__ascending - 1) < 0:
                        newNode.next = node.next
                        newNode.prev = node
                        node.next.prev = newNode
                        node.next = newNode
                        self.length += 1
                        return
            node = node.next
        # автоматическая вставка value
        # в нужную позицию

    def find(self, val):
        node = self.head
        while node is not None:
            if self.compare(node,Node(val))*(2*self.__ascending - 1) > 0:
                return None
            if node.value == val:
                return node
            node = node.next
        return None

    def delete(self, val):
        node = self.head
        while node is not None:
            if self.compare(node,Node(val))*(2*self.__ascending - 1) > 0:
                return
            if node.value == val:
                if node.next is not None:
                    if node.prev is None:
                        self.head = node.next
                        self.head.prev = None
                        self.length -= 1
                        return
                    else:
                        node.next.prev = node.prev
                        node.prev.next = node.next
                        self.length -= 1
                        return
                else:
                    if node.prev is not None:
                        self.tail = node.prev
                        self.tail.next = None
                        self.length -= 1
                        return
                    else:
                        self.head = None
                        self.tail = None
                        self.length -= 1
                        return
            node = node.next

    def clean(self, asc):
        self.__ascending = asc
        self.head = None
        self.tail = None
        self.length = 0
        pass # здесь будет ваш код

    def len(self):
        return self.length

    def get_all(self):
        r = []
        node = self.head
        while node != None:
            r.append(node)
            node = node.next
        return r

class OrderedStringList(OrderedList):
    def __init__(self, asc):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1, v2):
        v1 = v1.value.strip()
        v2 = v2.value.strip()
        v1l = len(v1)
        v2l = len(v2)
        if v1l > v2l:
            return 1
        elif v1l < v2l:
            return -1
        # переопределённая версия для строк
        for i in range(v1l):
            if v1[i] > v2[i]:
                return 1
            elif v1[i] < v2[i]:
                return -1
        return 0


