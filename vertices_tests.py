from weakvertices import *
import unittest

class testGraph(unittest.TestCase):

    def testWeakVertices(self):
        size = 15
        self.testGraph = SimpleGraph(size)
        for ii in range(12):
            self.testGraph.AddVertex(ii+1)
        self.testGraph.AddEdge(0, 1)
        self.testGraph.AddEdge(0, 3)
        self.testGraph.AddEdge(0, 5)
        self.testGraph.AddEdge(1, 2)
        self.testGraph.AddEdge(1, 3)
        self.testGraph.AddEdge(2, 3)
        self.testGraph.AddEdge(2, 4)
        self.testGraph.AddEdge(3, 5)
        self.testGraph.AddEdge(3, 4)
        self.testGraph.AddEdge(3, 7)
        self.testGraph.AddEdge(4, 7)
        self.testGraph.AddEdge(4, 11)
        self.testGraph.AddEdge(5, 6)
        self.testGraph.AddEdge(6, 7)
        self.testGraph.AddEdge(6, 8)
        self.testGraph.AddEdge(7, 9)
        self.testGraph.AddEdge(7, 10)
        self.testGraph.AddEdge(8, 9)
        self.testGraph.AddEdge(9, 10)
        self.testGraph.AddEdge(10,11)
        #print('Adjasencies: ')
        #for ii in range(self.testGraph.max_vertex):
        #    if self.testGraph.vertex[ii] is not None:
        #        adjs = []
        #        for jj in range(self.testGraph.max_vertex):
        #            if self.testGraph.IsEdge(ii,jj):
        #                adjs.append(jj+1)
        #        print(str(ii+1)+' : '+str(adjs))
        #a = self.testGraph.WeakVertices()
        self.assertEqual(self.testGraph.vertex[0].Value, 1, 'test root')
        self.assertEqual(self.testGraph.m_adjacency[0], [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'test adj0')
        self.assertEqual(self.testGraph.m_adjacency[7], [0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], 'test adj1')
        self.assertEqual(self.testGraph.vertex[6].Value, 7, 'test vertex')
        self.assertEqual(self.testGraph.WeakVertices(), [self.testGraph.vertex[6], self.testGraph.vertex[8],
                                                         self.testGraph.vertex[11]], 'test WeakVertices0')

unittest.main(verbosity=2)