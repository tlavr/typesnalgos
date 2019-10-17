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
        return None # если стек пустой

    def push(self, value):
        self.stack.add_in_head(Node(value))

    def peek(self):
        if self.size() > 0:
            ans = self.stack.head.value
            return ans
        return None # если стек пустой

class StackFIFO(Stack):
    def push(self, value):
        self.stack.add_in_tail(Node(value)) # для номера 2, где FIFO