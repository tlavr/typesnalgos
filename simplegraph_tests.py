from simplegraph import *
import unittest

class testGraph(unittest.TestCase):

    def testAdd(self):
        size = 3
        self.testGraph = SimpleGraph(size)
        self.testGraph.AddVertex(5)
        self.assertEqual(self.testGraph.vertex[0].Value, 5, 'test 1')
        self.assertEqual(self.testGraph.m_adjacency[0], [0] * size, 'test 1')

    def testAddEdge(self):
        size = 3
        self.testGraph = SimpleGraph(size)
        self.testGraph.AddVertex(5)
        self.testGraph.AddVertex(8)
        self.testGraph.AddEdge(0,1)
        self.assertTrue(self.testGraph.IsEdge(0,1),'test 2')
        self.assertEqual(self.testGraph.m_adjacency[0][1],1,'test 2')
        self.assertEqual(self.testGraph.m_adjacency[1][0], 1, 'test 2')

    def testRemove(self):
        size = 3
        self.testGraph = SimpleGraph(size)
        self.testGraph.AddVertex(5)
        self.testGraph.AddVertex(8)
        self.testGraph.AddVertex(2)
        self.testGraph.AddEdge(0, 1)
        self.testGraph.AddEdge(0, 2)
        self.testGraph.AddEdge(1, 2)
        self.testGraph.RemoveEdge(0,1)
        self.assertFalse(self.testGraph.IsEdge(0, 1), 'test 3')
        self.testGraph.AddEdge(0, 1)
        self.testGraph.RemoveVertex(1)
        self.assertEqual(self.testGraph.m_adjacency[1], [0] * size, 'test 3')
        self.assertFalse(self.testGraph.IsEdge(0, 1), 'test 3')
        self.assertFalse(self.testGraph.IsEdge(2, 1), 'test 3')


unittest.main(verbosity=2)
