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


unittest.main(verbosity=2)
