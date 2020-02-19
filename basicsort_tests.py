from basicsort import *
import unittest

class testSort(unittest.TestCase):
    def testSelection(self):
        self.a = [1,4,2,3,5,6]
        SelectionSortStep(self.a, 1)
        self.assertEqual(self.a,[1,2,4,3,5,6],'seltest1')

    def testBubble(self):
        self.a = [1, 4, 2, 3, 5, 6]
        self.assertFalse(BubbleSortStep(self.a))

print('5')
unittest.main(verbosity=2)
