#!/usr/bin/env python
#-*- coding: utf-8 -*-

from linked_lists import *

def check_find(test_num,val,check_list,find_test):
    print('found list:',find_test.find_all(val),'\n')
    if find_test.find_all(val) == check_list:
        print('Test ',test_num,' is ok!\n')
    else:
        print('Test ',test_num,' NOT ok!\n')        

find_test = LinkedList()

#св список пуст
check_find(1.1,5,[],find_test)
check_find(1.2,5,[],find_test)

#в св списке 1 элемент
find_test.add_in_tail(Node(1))
check_find(2.1,1,[1],find_test)
check_find(2.2,5,[],find_test)

#в св списке много элементов
check_4 = []
check_5 = []
for i in range(100):
    if i % 2 == 0:
        find_test.add_in_tail(Node(5))
        check_5.append(5)
    else:
        find_test.add_in_tail(Node(4))
        check_4.append(4)
find_test.add_in_tail(Node(3))
find_test.add_in_tail(Node(1))
find_test.insert(find_test.find(4),Node(2))
#find_test.print_all_nodes()
check_find(3.1,0,[],find_test)
check_find(3.2,1,[1,1],find_test)
check_find(3.3,3,[3],find_test)
check_find(3.4,4,check_4,find_test)
check_find(3.5,5,check_5,find_test)
