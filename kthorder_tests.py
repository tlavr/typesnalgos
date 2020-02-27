from kthOrderStatistics import *
import unittest

class testSort(unittest.TestCase):
    def testChunk(self):
        self.a = [7,5,6,4,3,1,2]
        self.assertEqual(KthOrderStatisticsStep(self.a, 0, self.a.__len__()-1, 3), [3, 3], 'orderIdx1')
        self.b = [7,6,4,5,2,3,1]
        self.assertEqual(KthOrderStatisticsStep(self.b, 0, self.b.__len__()-1, 3), [2, self.b.__len__()-1], 'orderIdx2')

unittest.main(verbosity=2)
