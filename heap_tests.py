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

    def checkOrder(self, h):
        ii = 0
        while ii < h.__size__:
            if 2*ii + 1 < h.__size__:
                if h.HeapArray[ii] < h.HeapArray[2*ii + 1]:
                    return False
            if 2*ii + 2 < h.__size__:
                if h.HeapArray[ii] < h.HeapArray[2*ii + 2]:
                    return False
            ii += 1
        return True

    def testMakeFull(self):
        self.testHeap = Heap()
        a = []
        d = 2
        for key in range(1,pow(2, d + 1)):
            a.append(key)
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.HeapArray,[7,4,6,1,3,2,5],'Full heap test')
        self.assertTrue(self.checkOrder(self.testHeap))

    def testMakeEmpty(self):
        self.testHeap = Heap()
        a = []
        d = 0
        self.testHeap.MakeHeap(a,d)
        self.assertEqual(self.testHeap.HeapArray,[],'Empty test')
        self.assertTrue(self.checkOrder(self.testHeap))

    def test1(self):
        self.testHeap = Heap()
        a = [110, 90, 40, 70, 80, 30, 10, 20, 50, 60, 65, 31, 29, 11, 9]
        self.testHeap.MakeHeap(a, 3)
        self.assertEqual(self.testHeap.HeapArray, [110,90,40,70,80,31,11,20,50,60,65,30,29,10,9], 'test 1')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.GetMax(), 110, 'get max test1')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.HeapArray, [90, 80, 31, 70, 65, 30, 10, 20, 50, 60, 40, 29, 11, 9],
                         'test 1')
        self.assertEqual(self.testHeap.GetMax(), 90, 'get max test2')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.HeapArray, [80, 70, 30, 65, 60, 29, 9, 20, 50, 40, 31, 11, 10],
                         'test 1')
        self.assertEqual(self.testHeap.GetMax(), 80, 'get max test')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertTrue(self.testHeap.Add(12))
        self.assertTrue(self.checkOrder(self.testHeap))

    def test2(self):
        self.testHeap = Heap()
        a = [90, 80, 40, 70, 65, 31, 11, 20, 50, 60, 9, 30, 29, 10]
        self.testHeap.MakeHeap(a, 3)
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.HeapArray, [90, 80, 40, 70, 65, 31, 11, 20, 50, 60, 9, 30, 29, 10], 'test 2')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.GetMax(), 90, 'get max test2')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.GetMax(), 80, 'get max test2')
        self.assertEqual(self.testHeap.HeapArray, [70, 65, 30, 60, 40, 29, 10, 20, 50, 31, 9, 11],
                         'test 2')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertTrue(self.testHeap.Add(12))
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.HeapArray, [70, 65, 30, 60, 40, 29, 10, 20, 50, 31, 9, 11, 12],
                         'test 2')
        #print_heap(self.testHeap.HeapArray, '2.3')

    def testAdd(self):
        self.testHeap = Heap()
        a = [11, 8, 6, 5, 4]
        self.testHeap.MakeHeap(a, 2)
        self.assertTrue(self.checkOrder(self.testHeap))
        self.testHeap.Add(12)
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.HeapArray, [12, 8, 11, 5, 4, 6], 'Add element test')

    def testGetMax(self):
        self.testHeap = Heap()
        a = []
        d = 2
        for key in range(1,pow(2, d + 1)):
            a.append(key)
        self.testHeap.MakeHeap(a,d)
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.GetMax(),7,'get max test')
        self.assertTrue(self.checkOrder(self.testHeap))
        self.assertEqual(self.testHeap.HeapArray, [6, 4, 5, 1, 3, 2], 'Full heap test')

unittest.main(verbosity=2)