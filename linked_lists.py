#!/usr/bin/env python
#-*- coding: utf-8 -*-

#import ctypes
# N = 5
# A = (N * ctypes.py_object)()

class Node:
    def __init__(self, v):
        self.value = v
        self.next = None

class LinkedList:  
    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item

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
                found.append(node.value)
            node = node.next
        return found

    def delete(self, val, all=False):
        node = self.head
        node_prev = None
        while node is not None:
            if node.value == val:
                if node.next is not None:
                    node.value = node.next.value
                    node.next = node.next.next
                    if all:
                        self.delete(val,True)
                    else:
                        return
                elif node_prev is not None:
                    self.tail = node_prev
                    self.tail.next = None
                    return
                else:
                    self.head = None
                    self.tail = None
                    return
            node_prev = node
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

    def insert(self, afterNode, nNode):
        node = self.head
        global newNode
        newNode = nNode
        while node is not None:
            print('i\'m here!',node.value)
            if self.head == None:
                if afterNode == None:
                    newNode.next = None
                    self.add_in_tail(newNode)
                    return
                
            if node == afterNode:
                if node.next is None:                  
                    self.add_in_tail(newNode)
                    return
                else:
                    newNode.next = node.next
                    node.next = newNode
                    return
            node = node.next
def sum_link_vals(a,b):
    global c
    c = LinkedList()
    if a.len() == b.len():
        node_a = a.head
        node_b = b.head
        while node_a is not None:
            c.add_in_tail(Node(node_a.value + node_b.value))
            node_a = node_a.next
            node_b = node_b.next
    else:
        print('Linked lists don\t have the same length!')
    return c


