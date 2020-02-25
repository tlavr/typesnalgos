from quicksort import *
import unittest

class testSort(unittest.TestCase):
    def testChunk(self):
        self.a = [7,5,6,4,3,1,2]
        self.assertEqual(ArrayChunk(self.a),3,'ChunkIdx1')
        self.assertEqual(self.a,[2,1,3,4,6,5,7],'Arr1')
        self.b = [7,6,4,5,2,3,1]
        self.assertEqual(ArrayChunk(self.b), 1, 'ChunkIdx2')
        self.assertEqual(self.b, [1, 2, 4, 3, 5, 6, 7], 'Arr2')
        self.c = [5, 2]
        self.assertEqual(ArrayChunk(self.c), 1)
        self.assertEqual(self.c, [2,5], 'Arr3')
        self.d = [7,6,5,4,3,2,1]
        self.e = [5,4,7,6,3,2,1]
        self.assertEqual(QuickSort(self.d), self.e.sort(), 'Quick1')

    def testTailOpt(self):
        self.d = [7,6,5,4,3,2,1]
        self.e = [5,4,7,6,3,2,1]
        self.assertEqual(QuickSortTailOptimization(self.d), self.e.sort(), 'QuickOpt1')
        self.f = [1, 6, 2, 4, 7, 8, 3, 5, 9, 0]
        self.g = [1, 6, 2, 4, 7, 8, 3, 5, 9, 0]
        self.assertEqual(QuickSortTailOptimization(self.f),self.g.sort(), 'QuickOpt2')

unittest.main(verbosity=2)
