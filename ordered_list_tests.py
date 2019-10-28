#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ordered_list import *


def print_list(a):
    for i in a.get_all():
        print(i.value)

def test_list(a,val,asc):
    try:
        #delete test
        a.delete(Node(val).value)

        #find tests
        print('\n find:',a.find(Node(val).value))

        #len test
        print('\n len:',a.len())

        #insert test
        a.add(-1)

        #print all test
        print('All nodes:')
        print_list(a)

        #clean test
        a.clean(asc)
        print('\n All nodes after cleaning:')
        print_list(a)
        print('\n List is ok!')
    except:
        print('\n Something gone wrong!')

asc = True
#empty list test
empty_list = OrderedList(asc)
test_list(empty_list,0,asc)
print('\n')

#one element list test
one_list = OrderedList(asc)
one_list.add_in_tail(Node(1))
test_list(one_list,1,asc)
print('\n')

#many elements list test
many_list = OrderedList(asc)
for i in range(10000):
    many_list.add(i)
    many_list.add(50-i)
test_list(many_list,19,asc)

ol = OrderedList(asc)
print('List: ')
ol.add(0)
print_list(ol)
print('List: ')
ol.add(100)
print_list(ol)
ol.add(-100)
print('List: ')
print_list(ol)
ol.clean(~asc)
print('List: ')
print_list(ol)
ol.add(0)
print('List: ')
print_list(ol)
ol.add(100)
print('List: ')
print_list(ol)
ol.add(-100)
print('List: ')
print_list(ol)

ostr = OrderedStringList(~asc)
ostr.add('abcd')
ostr.add('aba')
ostr.add('abb')
print_list(ostr)
