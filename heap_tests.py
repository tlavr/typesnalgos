import unittest
from heap import *

class testHeap(unittest.TestCase):

    def testMakeFull(self):
        self.testHeap = Heap()
        a = []
        d = 2
        for key in range(1,pow(2, d + 1)):
            a.append(key)
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.HeapArray,[7,6,5,4,3,2,1],'Full heap test')

    def testMakeEmpty(self):
        self.testHeap = Heap()
        a = []
        d = 0
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.HeapArray,[],'Empty test')

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