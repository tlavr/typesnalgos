from mergesort import *
import unittest
import random

class testSort(unittest.TestCase):
    def testMerge(self):
        self.a = [7,5,6,4,3,1,2]
        self.b = [7,5,6,4,3,1,2]
        self.b.sort()
        self.assertEqual(MergeSort(self.a), self.b, 'Merge1')
        self.c = [7,6,4,5,2,3,1]
        self.d = [7,6,4,5,2,3,1]
        self.d.sort()
        self.assertEqual(MergeSort(self.c), self.d, 'Merge2')
        self.e = [2,1,4,12,54,21,234,66,11,13,98,73]
        self.f = [2,1,4,12,54,21,234,66,11,13,98,73]
        self.f.sort()
        self.assertEqual(MergeSort(self.e), self.f, 'Merge3')
        self.g = [2]
        self.h = [2]
        self.h.sort()
        self.assertEqual(MergeSort(self.g), self.h, 'Merge4')
        self.i = []
        self.j = []
        self.j.sort()
        self.assertEqual(MergeSort(self.i), self.j, 'Merge5')
        self.k = []
        self.l = []
        for ii in range(10000):
            el = random.randint(0,1000)
            self.k.append(el)
            self.l.append(el)
        self.l.sort()
        self.assertEqual(MergeSort(self.k), self.l, 'Merge6')


unittest.main(verbosity=2)
