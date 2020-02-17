from dfs import *
import unittest
"""
size = 15
testGraph = SimpleGraph(size)
for ii in range(10):
    testGraph.AddVertex(ii+1)
    if ii > 0:
        testGraph.AddEdge(ii-1,ii)
testGraph.AddEdge(0, 9)
print(testGraph.DepthFirstSearch(2,6))

"""
class testGraph(unittest.TestCase):

    def testDFS(self):
        size = 15
        self.testGraph = SimpleGraph(size)
        for ii in range(10):
            self.testGraph.AddVertex(ii+1)
            if ii > 0:
                self.testGraph.AddEdge(ii-1,ii)
        self.testGraph.AddEdge(0, 9)
        self.assertEqual(self.testGraph.vertex[0].Value, 1, 'test root')
        self.assertEqual(self.testGraph.m_adjacency[0], [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0], 'test adj')
        self.assertEqual(self.testGraph.vertex[6].Value, 7, 'test vertex')
        self.assertEqual(self.testGraph.DepthFirstSearch(2,6),[2,1,0,9,8,7,6],'test DFS')
        self.testGraph.AddEdge(9, 7)
        self.testGraph.AddEdge(1, 9)
        self.testGraph.AddEdge(3, 1)
        self.testGraph.AddEdge(5, 3)
        self.testGraph.AddEdge(5, 7)
        self.assertEqual(self.testGraph.DepthFirstSearch(2, 6), [2, 1,0, 9, 7, 6], 'test DFS')

unittest.main(verbosity=2)