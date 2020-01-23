import unittest
from heap import *

def print_heap(h,s):
    print(s+' heap elements:')
    if h.__len__() > 0:
        ii = 0
        for key in h:
            print(str(ii) + ' : ' + str(key))
            ii += 1

class testHeap(unittest.TestCase):

    def testMakeFull(self):
        self.testHeap = Heap()
        a = []
        d = 2
        for key in range(1,pow(2, d + 1)):
            a.append(key)
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.HeapArray,[7,4,6,1,3,2,5],'Full heap test')

    def testMakeEmpty(self):
        self.testHeap = Heap()
        a = []
        d = 0
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.HeapArray,[],'Empty test')

    def test1(self):
        self.testHeap = Heap()
        a = [110, 90, 40, 70, 80, 30, 10, 20, 50, 60, 65, 31, 29, 11, 9]
        self.testHeap.MakeHeap(a, 3)
        self.assertFalse(self.testHeap.Add(12))
        self.assertEqual(self.testHeap.HeapArray, [110,90,40,70,80,31,11,20,50,60,65,30,29,10,9], 'test 1')
        self.assertEqual(self.testHeap.GetMax(), 110, 'get max test1')
        self.assertEqual(self.testHeap.GetMax(), 90, 'get max test2')
        self.assertEqual(self.testHeap.GetMax(), 80, 'get max test')
        self.assertTrue(self.testHeap.Add(12))


    def testAdd(self):
        self.testHeap = Heap()
        a = [11, 8, 6, 5, 4]
        self.testHeap.MakeHeap(a, 2)
        self.testHeap.Add(12)
        self.assertEqual(self.testHeap.HeapArray, [12, 8, 11, 5, 4, 6, None], 'Add element test')

    def testGetMax(self):
        self.testHeap = Heap()
        a = []
        d = 2
        for key in range(1,pow(2, d + 1)):
            a.append(key)
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.GetMax(),7,'get max test')
        self.assertEqual(self.testHeap.HeapArray, [6, 4, 5, 1, 3, 2, None], 'Full heap test')

unittest.main(verbosity=2)