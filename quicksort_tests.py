from quicksort import *
import unittest

class testSort(unittest.TestCase):
    def testChunk(self):
        self.a = [7,5,6,4,3,1,2]
        self.assertEqual(ArrayChunk(self.a),3,'ChunkIdx1')
        self.assertEqual(self.a,[2,1,3,4,6,5,7],'Arr1')


unittest.main(verbosity=2)
