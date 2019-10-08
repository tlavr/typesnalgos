#!/usr/bin/env python
#-*- coding: utf-8 -*-

#import importlib
#moduleName = 'linked_lists'
#importlib.import_module(moduleName)

from linked_lists import *

def test_list(a):
    tmp = Node(0)
    try:
        a.delete(tmp.value)
        a.delete(tmp.value,True)
        print('\n find:',a.find(tmp))
        print('\n find all:',a.find_all(tmp.value))
        print('\n len:',a.len())
        a.insert(a.find(tmp),tmp)
        a.add_in_tail(tmp)
        print('\n All nodes: \n')
        a.print_all_nodes()
        a.clean()
        print('\n List is ok!')
    except:
        print('\n Something gone wrong!')

n1 = Node(12)

one_list = LinkedList()
empty_list = LinkedList()
many_list = LinkedList()
sum_list = LinkedList()

one_list.add_in_tail(n1)

for i in range(100):
    many_list.add_in_tail(Node(i))

test_list(one_list)
print('\n')
test_list(empty_list)
print('\n')
test_list(many_list)

sum_list = sum_link_vals(many_list, many_list)
print('\n')
sum_list.print_all_nodes()
