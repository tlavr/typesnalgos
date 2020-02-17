class SimpleTreeNode:
    def __init__(self, val, parent):
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.Children = []  # список дочерних узлов
        self.lvl = 0


class SimpleTree:
    def __init__(self, root):
        self.Root = root  # корень, может быть None
        self.__allNodes__ = []
        self.__setNodeLvl__(root,1)
        self.__nodesToDel__ = []

    def __setNodeLvl__(self,parentNode,lvl):
        parentNode.lvl = lvl
        if parentNode.Children.__len__() != 0:
            for node in parentNode.Children:
                self.__setNodeLvl__(node,lvl+1)

    def AddChild(self, ParentNode, NewChild):
        # ваш код добавления нового дочернего узла существующему ParentNode
        ParentNode.Children.append(NewChild)
        NewChild.Parent = ParentNode
        self.__setNodeLvl__(NewChild,ParentNode.lvl+1)

    def DeleteNode(self, NodeToDelete):
        # ваш код удаления существующего узла NodeToDelete
        if self.Root is NodeToDelete:
            self.Root = None
        else:
            PNode = NodeToDelete.Parent
            PNode.Children.remove(NodeToDelete)
            if NodeToDelete.Children.__len__() != 0:
                for Node in NodeToDelete.Children:
                    Node.Parent = PNode
                    PNode.Children.append(Node)

    def GetAllNodes(self, parentNode = None, isFirst = True):
        # ваш код выдачи всех узлов дерева в определённом порядке
        if isFirst:
            self.__allNodes__ = []
        if parentNode is None:
            parentNode = self.Root
        if parentNode is not None:
            self.__allNodes__.append(parentNode)
            if parentNode.Children.__len__() != 0:
                for node in parentNode.Children:
                    self.GetAllNodes(node, False)
        return self.__allNodes__

    def FindNodesByValue(self, val):
        valNodes = []
        # ваш код поиска узлов по значению
        nodes = self.GetAllNodes()
        for node in nodes:
            if node.NodeValue == val:
                valNodes.append(node)
        return valNodes

    def MoveNode(self, OriginalNode, NewParent):
        # ваш код перемещения узла вместе с его поддеревом --
        # в качестве дочернего для узла NewParent
        OriginalNode.Parent.Children.remove(OriginalNode)
        self.AddChild(NewParent,OriginalNode)

    def Count(self, fromNode = None):
        # количество всех узлов в дереве / поддереве
        self.GetAllNodes(fromNode, True)
        return self.__allNodes__.__len__()

    def LeafCount(self):
        # количество листьев в дереве / поддереве
        self.GetAllNodes()
        leavescnt = 0
        for node in self.__allNodes__:
            if node.Children.__len__() == 0:
                leavescnt += 1
        return leavescnt

    def EvenTrees(self, fromNode = None):
        if fromNode is None:
            fromNode = self.Root
            self.__nodesToDel__ = []
        if self.Count(fromNode) % 2 == 0:
            if fromNode.Parent is not None:
                self.__nodesToDel__.append(fromNode.Parent)
                self.__nodesToDel__.append(fromNode)
            for node in fromNode.Children:
                self.EvenTrees(node)
        return self.__nodesToDel__


"""
    def __getAllChild__(self,parentNode, isFirst = True):
        if isFirst:
            self.__allNodes__ = []
        self.__allNodes__.append(parentNode)
        if parentNode.Children.__len__() != 0:
            for node in parentNode.Children:
                self.__getAllChild__(node, False)

    def __makeOneList__(self,nodes):
        outlist = []
        for node in nodes:
            if type(node) is list:
                for nnode in node:
                    outlist.append(nnode)
            else:
                outlist.append(node)
        return outlist

    def __countLists__(self,nodes):
        ans = 0
        for node in nodes:
            if type(node) is list:
                ans += 1
        return ans
"""