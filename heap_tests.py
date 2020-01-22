from heap import *

def print_heap(h,s):
    print(s + ' heap elements: ')
    i = 0
    for key in h:
        print(str(i)+' : '+str(key))
        i += 1

testHeap = Heap()
print_heap(testHeap.HeapArray,'Empty')

a = []
d = 3
for key in range(pow(2,d+1)-1):
    a.append(key)
testHeap.MakeHeap(a,d)
print_heap(testHeap.HeapArray,'Full')
print('Max: '+str(testHeap.GetMax()))
print_heap(testHeap.HeapArray,'Full')

testHeap = Heap()
a = [11,9,4,7,8,3,1,2,5,6]
testHeap.MakeHeap(a,3)
print_heap(testHeap.HeapArray,'Half full')
print('Max: '+str(testHeap.GetMax()))
testHeap.Add(10)
testHeap.Add(12)
print_heap(testHeap.HeapArray,'Half full')
