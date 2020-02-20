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

    def testInsertion(self):
        self.a = [1,6,5,4,3,2,7]
        InsertionSortStep(self.a, 3, 1)
        self.assertEqual(self.a,[1,3,5,4,6,2,7],'instest1')
        InsertionSortStep(self.a, 1, 2)
        self.assertEqual(self.a, [1, 3, 2, 4, 5, 6, 7], 'instest2')
        self.b = [7,6,5,4,3,2,1]
        InsertionSortStep(self.b, 3, 0)
        self.assertEqual(self.b,[1,6,5,4,3,2,7], 'instest3')

print('5')
unittest.main(verbosity=2)
