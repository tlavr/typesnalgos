from ShellSort import *
import unittest

class testSort(unittest.TestCase):
    def testSelection(self):
        self.a = [1,4,2,3,5,6]
        SelectionSortStep(self.a, 1)
        self.assertEqual(self.a,[1,2,4,3,5,6],'seltest1')
        self.a = [1, 4, 2, 3, 5, 6]
        self.c = [1, 4, 2, 3, 5, 6]
        self.assertEqual(SelectionSort(self.a), self.c.sort(), 'sel1')

    def testBubble(self):
        self.a = [1, 4, 2, 3, 5, 6]
        self.assertFalse(BubbleSortStep(self.a))
        self.a = [1, 4, 2, 3, 5, 6]
        self.c = [1, 4, 2, 3, 5, 6]
        self.assertEqual(BubbleSort(self.a), self.c.sort(), 'Bubble1')

    def testInsertion(self):
        self.a = [1,6,5,4,3,2,7]
        InsertionSortStep(self.a, 3, 1)
        self.assertEqual(self.a,[1,3,5,4,6,2,7],'instest1')
        InsertionSortStep(self.a, 1, 2)
        self.assertEqual(self.a, [1, 3, 2, 4, 5, 6, 7], 'instest2')
        self.b = [7,6,5,4,3,2,1]
        InsertionSortStep(self.b, 3, 0)
        self.assertEqual(self.b,[1,6,5,4,3,2,7], 'instest3')
        self.a = [1, 4, 2, 3, 5, 6]
        self.c = [1, 4, 2, 3, 5, 6]
        self.assertEqual(InsertionSort(self.a), self.c.sort(), 'Insert1')

    def testKnuth(self):
        self.assertEqual(KnuthSequence(15),[13,4,1],'Knuth1')
        self.assertEqual(KnuthSequence(14), [13, 4, 1], 'Knuth2')
        self.assertEqual(KnuthSequence(13), [13, 4, 1], 'Knuth3')
        self.assertEqual(KnuthSequence(0), [], 'Knuth4')
        self.assertEqual(KnuthSequence(1), [1], 'Knuth5')
        self.assertEqual(KnuthSequence(40), [40, 13, 4, 1], 'Knuth1')

    def testShellSort(self):
        self.a = [1,12,2,1,2,5,2,1,3,5,1,2,213,1,2,42,51,123,2,1,5,2,1,213,12,6,213,8,2,34,52,4,543,124,122,6,21,3]
        self.c = [1,12,2,1,2,5,2,1,3,5,1,2,213,1,2,42,51,123,2,1,5,2,1,213,12,6,213,8,2,34,52,4,543,124,122,6,21,3]
        self.assertEqual(ShellSort(self.a), self.c.sort(), 'Shell1')


unittest.main(verbosity=2)
