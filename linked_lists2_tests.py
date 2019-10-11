#!/usr/bin/env python
#-*- coding: utf-8 -*-

#import importlib
#moduleName = 'linked_lists'
#importlib.import_module(moduleName)

from linked_lists2 import *

def test_list(a,val):
    tmp = Node(val)
    try:
        #delete test
        a.delete(Node(val).value)
        if val > 0:
            a.add_in_tail(Node(val))
        a.delete(Node(val).value,True)
        if val > 0:
            a.add_in_tail(Node(val))
        #find tests
        print('\n find:',a.find(Node(val).value))
        print('\n find all:',a.find_all(Node(val).value))
        #len test
        print('\n len:',a.len())
        #insert test
        a.insert(a.find(val),Node(2))
        a.delete(Node(val).value)
        #add in tail test
        a.add_in_tail(Node(val))
        a.delete(Node(val).value)
        #add in head test
        a.add_in_head(Node(val))
        a.delete(Node(val).value)
        #print all test
        print('\n All nodes:')
        a.print_all_nodes()
        #clean test
        a.clean()
        print('\n All nodes after cleaning:')
        a.print_all_nodes()
        print('\n List is ok!')
    except:
        print('\n Something gone wrong!')

#empty list test
empty_list = LinkedList2()
test_list(empty_list,0)
print('\n')

#one element list test
one_list = LinkedList2()
one_list.add_in_tail(Node(1))
test_list(one_list,1)
print('\n')

#many elements list test
many_list = LinkedList2()
for i in range(100):
    many_list.add_in_tail(Node(i % 20))
test_list(many_list,19)


