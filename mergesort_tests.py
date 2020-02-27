from mergesort import *
import unittest

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


unittest.main(verbosity=2)
