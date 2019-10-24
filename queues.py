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