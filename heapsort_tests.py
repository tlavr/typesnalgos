from heapsort import *
import unittest
import random

class testHeap(unittest.TestCase):
    def testSort(self):
        self.a = [7, 5, 6, 4, 3, 1, 2]
        self.b = [7, 5, 6, 4, 3, 1, 2]
        self.b.sort()
        self.assertEqual(HeapSort(self.a).GetNextMax(), self.b, 'Heap1')
        self.c = [7, 6, 4, 5, 2, 3, 1]
        self.d = [7, 6, 4, 5, 2, 3, 1]
        self.d.sort()
        self.assertEqual(HeapSort(self.c).GetNextMax(), self.d, 'Heap2')
        self.e = [2, 1, 4, 12, 54, 21, 234, 66, 11, 13, 98, 73]
        self.f = [2, 1, 4, 12, 54, 21, 234, 66, 11, 13, 98, 73]
        self.f.sort()
        self.assertEqual(HeapSort(self.e).GetNextMax(), self.f, 'Heap3')
        self.g = [2]
        self.h = [2]
        self.h.sort()
        self.assertEqual(HeapSort(self.g).GetNextMax(), self.h, 'Heap4')
        self.i = []
        self.j = []
        self.j.sort()
        self.assertEqual(HeapSort(self.i).GetNextMax(), self.j, 'Heap5')
        self.k = []
        self.l = []
        for ii in range(100000):
            el = random.randint(0, 10000)
            self.k.append(el)
            self.l.append(el)
        self.l.sort()
        self.assertEqual(HeapSort(self.k).GetNextMax(), self.l, 'Heap6')


unittest.main(verbosity=2)