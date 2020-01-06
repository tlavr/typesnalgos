class BSTNode:
    def __init__(self, key, val, parent):
        self.NodeKey = key  # ключ узла
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.LeftChild = None  # левый потомок
        self.RightChild = None  # правый потомок


class BSTFind:  # промежуточный результат поиска
    def __init__(self):
        self.Node = None  # None если
        # в дереве вообще нету узлов
        self.NodeHasKey = False  # True если узел найден
        self.ToLeft = False  # True, если родительскому узлу надо
        # добавить новый узел левым потомком


class BST:
    def __init__(self, node):
        self.Root = node  # корень дерева, или None
        self.allNodes = []
        if node is not None:
            self.__len__ = 1
        else:
            self.__len__ = 0

    def FindNodeByKey(self, key):
        # ищем в дереве узел и сопутствующую информацию по ключу
        curNode = self.Root
        foundNode = BSTFind()
        while curNode is not None:
            if key == curNode.NodeKey:
                foundNode.Node = curNode
                foundNode.NodeHasKey = True
                curNode = None
            elif key > curNode.NodeKey:
                if curNode.RightChild is not None:
                    curNode = curNode.RightChild
                else:
                    foundNode.Node = curNode
                    curNode = None
            else:
                if curNode.LeftChild is not None:
                    curNode = curNode.LeftChild
                else:
                    foundNode.Node = curNode
                    foundNode.ToLeft = True
                    curNode = None
        return foundNode # возвращает BSTFind

    def AddKeyValue(self, key, val):
        # добавляем ключ-значение в дерево
        addNode = BSTNode(key,val,None)
        foundNode = self.FindNodeByKey(key)
        if foundNode.Node is None:
            self.Root = addNode
            self.__len__ += 1
        elif foundNode.NodeHasKey is True:
            return False  # если ключ уже есть
        else:
            addNode.Parent = foundNode.Node
            if foundNode.ToLeft is True:
                foundNode.Node.LeftChild = addNode
            else:
                foundNode.Node.RightChild = addNode
            self.__len__ += 1
            return True

    def FinMinMax(self, FromNode, FindMax):
        # ищем максимальное/минимальное (узел) в поддереве
        foundNode = None
        if FromNode is not None:
            if FindMax is False:
                while FromNode.LeftChild is not None:
                    FromNode = FromNode.LeftChild
            else:
                while FromNode.RightChild is not None:
                    FromNode = FromNode.RightChild
            foundNode = FromNode
        return foundNode

    def __isLeaf__(self,node): # 0 -> Leaf, 1 -> has only LeftChild, 2 -> has only RightChild, 3 -> both
        if node.LeftChild is None and node.RightChild is None:
            return 0
        elif node.RightChild is None:
            return 1
        elif node.LeftChild is None:
            return 2
        else:
            return 3

    def __isLeftChild__(self,parentNode,node):
        # determine left or right child
        if parentNode.LeftChild is node:
            return True
        elif parentNode.RightChild is node:
            return False
        else:
            return None

    def DeleteNodeByKey(self, key,out = True):
        # удаляем узел по ключу
        nodeToDel = self.FindNodeByKey(key)
        if nodeToDel.Node is None or nodeToDel.NodeHasKey is False:
            return False  # если узел не найден
        else:
            nodeToDel = nodeToDel.Node
            cond = self.__isLeaf__(nodeToDel)
            if cond == 0: # if node is a leaf
                if self.__isLeftChild__(nodeToDel.Parent, nodeToDel):
                    nodeToDel.Parent.LeftChild = None
                else:
                    nodeToDel.Parent.RightChild = None
            elif cond == 1: # if node has one left child
                if self.__isLeftChild__(nodeToDel.Parent, nodeToDel):
                    nodeToDel.Parent.LeftChild = nodeToDel.LeftChild
                else:
                    nodeToDel.Parent.RightChild = nodeToDel.LeftChild
                nodeToDel.LeftChild.Parent = nodeToDel.Parent
            elif cond == 2: # if node has one right child
                if self.__isLeftChild__(nodeToDel.Parent, nodeToDel):
                    nodeToDel.Parent.LeftChild = nodeToDel.RightChild
                else:
                    nodeToDel.Parent.RightChild = nodeToDel.RightChild
                nodeToDel.RightChild.Parent = nodeToDel.Parent
            else: # if node has both children
                minNode = self.FinMinMax(nodeToDel.RightChild,False) # find the most left node on the right side
                tmpBool = self.DeleteNodeByKey(minNode.NodeKey,False)
                if self.__isLeftChild__(nodeToDel.Parent, nodeToDel):
                    nodeToDel.Parent.LeftChild = minNode
                else:
                    nodeToDel.Parent.RightChild = minNode
                minNode.RightChild = nodeToDel.RightChild
                minNode.LeftChild = nodeToDel.LeftChild
                minNode.Parent = nodeToDel.Parent
            if out is True:
                self.__len__ -= 1
            return True

    def __collectAllNodes__(self,fromNode = None):
        if fromNode is None or fromNode is self.Root:
            fromNode = self.Root
            self.allNodes = []
        self.allNodes.append(fromNode)
        if fromNode.LeftChild is not None:
            self.__collectAllNodes__(fromNode.LeftChild)
        if fromNode.RightChild is not None:
            self.__collectAllNodes__(fromNode.RightChild)

    def getAllNodes(self):
        self.__collectAllNodes__()
        return self.allNodes

    def Count(self):
        return self.__len__  # количество узлов в дереве