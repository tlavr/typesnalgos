from galloping_search import *
import unittest

class testBinSearch(unittest.TestCase):
    def testSearch(self):
        self.a = [ii for ii in range(30)]
        self.assertTrue(GallopingSearch(self.a, 14), 'test1')
        self.assertFalse(GallopingSearch(self.a, 30), 'test2')
        self.a = [ii for ii in range(1, 1000000)]
        self.assertTrue(GallopingSearch(self.a, 910233), 'test3')
        self.assertFalse(GallopingSearch(self.a, 100000001), 'test4')
        self.a = [1, 3, 4]
        self.assertTrue(GallopingSearch(self.a, 3), 'test5')
        self.assertTrue(GallopingSearch(self.a, 4), 'test6')
        self.assertFalse(GallopingSearch(self.a, 5), 'test7')
        self.a = [1]
        self.assertTrue(GallopingSearch(self.a, 1), 'test8')
        self.assertFalse(GallopingSearch(self.a, 0), 'test9')
        self.a = []
        self.assertFalse(GallopingSearch(self.a, 5), 'test10')


unittest.main(verbosity=2)