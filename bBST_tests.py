from bBST_func import *
import random

a = [] # not full: 1 element in the left subtree , 1 in the right
b = [] # full
c = [] # with one more level in the left subtree
for ii in range(1,10):
    a.append(ii)
for ii in range(1,16):
    b.append(ii)
    c.append(ii)
c.append(16)
random.shuffle(a)
random.shuffle(b)
random.shuffle(c)
print('a: '+str(a))
print('b: '+str(b))
print('b: '+str(c))

a_out = GenerateBBSTArray(a)
print('a_out :'+str(a_out))
b_out = GenerateBBSTArray(b)
print('b_out :'+str(b_out))
c_out = GenerateBBSTArray(c)
print('c_out :'+str(c_out))