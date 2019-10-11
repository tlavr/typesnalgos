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
    
    def print_all_nodes(self):
        node = self.head
        while node is not None:
            print(node.value)
            node = node.next

    def find(self, val):
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val):
        found = []
        node = self.head
        while node is not None:
            if node.value == val:
                found.append(node)
            node = node.next
        return found

    def delete(self, val, all=False):
        node = self.head
        while node is not None:
            if node.value == val:
                if node.next is not None:
                    if node.prev is None:
                        self.head = node.next
                        self.head.prev = None
                        if all:
                            self.delete(val,True)
                        else:
                            return
                    else:
                        node.next.prev = node.prev
                        node.prev.next = node.next
                        if all:
                            self.delete(val,True)
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

    def clean(self):
        self.head = None
        self.tail = None

    def len(self):
        ans = 0
        node = self.head
        while node is not None:
            ans += 1
            node = node.next          
        return ans

    def insert(self, afterNode, newNode):
        newNode.next = None
        newNode.prev = None
        if afterNode is None:
            self.add_in_tail(newNode)
            return
        
        node = self.head
        while node is not None:   
            if node is afterNode:
                if node.next is None:
                    self.add_in_tail(newNode)
                    return
                else:
                    newNode.next = node.next
                    newNode.prev = node
                    node.next.prev = newNode
                    node.next = newNode
                    return
            node = node.next
        

