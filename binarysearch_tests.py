from binary_search import *
import unittest

class testBinSearch(unittest.TestCase):
    def testSearch(self):
        self.a = [ii for ii in range(30)]
        self.bs = BinarySearch(self.a)
        self.bs.Step(14)
        self.assertEqual(self.bs.GetResult(),1,'test1')
        self.bs = BinarySearch(self.a)
        self.bs.Step(15)
        self.assertEqual(self.bs.GetResult(), 0, 'test2')
        self.bs = BinarySearch(self.a)
        while self.bs.GetResult() == 0:
            self.bs.Step(31)
        self.assertEqual(self.bs.GetResult(), -1, 'test3')
        self.bs = BinarySearch(self.a)
        while self.bs.GetResult() != 1:
            self.assertEqual(self.bs.GetResult(), 0, 'test4')
            self.bs.Step(2)
        self.assertEqual(self.bs.GetResult(), 1, 'test5')
        self.bs = BinarySearch([1])
        self.bs.Step(2)
        self.assertEqual(self.bs.GetResult(), -1, 'test6')
        self.bs = BinarySearch([1])
        self.bs.Step(1)
        self.assertEqual(self.bs.GetResult(), 1, 'test7')
        self.bs = BinarySearch([])
        self.bs.Step(1)
        self.assertEqual(self.bs.GetResult(), -1, 'test7')

unittest.main(verbosity=2)