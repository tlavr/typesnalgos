#!/usr/bin/env python
#-*- coding: utf-8 -*-

#import importlib
moduleName = 'linked_lists'
#importlib.import_module(moduleName)

from linked_lists import *

n1 = Node(12)
n2 = Node(55)
n3 = Node(33)
n1.next = n2 # 12 -> 55

s_list = LinkedList()
sum_list = LinkedList()

s_list.add_in_tail(n1)
s_list.add_in_tail(Node(128))
s_list.add_in_tail(n2)
s_list.print_all_nodes()
print('\n')
print('len is:',s_list.len())
s_list.delete(128)
#s_list.delete(55)
#s_list.delete(121)
#s_list.clean()
print(s_list.find_all(128))
print(s_list.find(55).value)
print('\n')
s_list.insert(s_list.find(55),n3)
print('len is:',s_list.len())
s_list.print_all_nodes()

sum_list = sum_link_vals(s_list, s_list)
print('\n')
sum_list.print_all_nodes()
