from ksort import *
import unittest

class testKsort(unittest.TestCase):
    def testSort(self):
        self.a = "abcdefgh"
        self.list = []
        self.k = ksort()
        for ii in range(8):
            for jj in range(10):
                for zz in range(10):
                    self.list.append(self.a[ii] + str(jj) + str(zz))
                    self.k.add(self.a[ii] + str(jj) + str(zz))
        self.assertEqual(self.k.items[1],"a01",'test1')
        self.assertEqual(self.k.items[99],"a99",'test2')
        self.assertEqual(self.k.items[565], "f65", 'test2')

unittest.main(verbosity=2)