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

    def delete(self, val, all=False, fromhead = True):
        if fromhead:
            node = self.head
        else:
            node = self.tail
        while node is not None:
            if node.value == val:
                if node.next is not None:
                    if node.prev is None:
                        self.head = node.next
                        self.head.prev = None
                        self.length  -= 1
                        if all:
                            if fromhead:
                                self.delete(val, True)
                            else:
                                self.delete(val,True,False)
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
                        if all:
                            if fromhead:
                                self.delete(val, True)
                            else:
                                self.delete(val,True,False)
                        else:
                            return
                        return
                    else:
                        self.head = None
                        self.tail = None
                        self.length  -= 1
                        return
            if fromhead:
                node = node.next
            else:
                node = node.prev

    def len(self):
        return self.length

class Deque:
    def __init__(self):
        self.deq = LinkedList2()

    def addFront(self, item):
        # добавление в голову
        self.deq.add_in_head(Node(item))


    def addTail(self, item):
        # добавление в хвост
        self.deq.add_in_tail(Node(item))

    def removeFront(self):
        # удаление из головы
        if self.size() > 0:
            ans = self.deq.head.value
            self.deq.delete(ans)
            return ans
        return None # если очередь пуста

    def removeTail(self):
        # удаление из хвоста
        if self.size() > 0:
            ans = self.deq.tail.value
            self.deq.delete(ans,False,False)
            return ans
        return None # если очередь пуста

    def size(self):
        return self.deq.len()

def ispalindrome(line,needup = False):
    deq = Deque()
    line = ''.join(line.split())
    if needup:
        line = line.upper()
    for i in line:
        deq.addTail(i)
    while deq.size() > 1:
        if deq.removeFront() != deq.removeTail():
            return False
    return True