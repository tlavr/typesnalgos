class SimpleTreeNode:
    def __init__(self, val, parent):
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.Children = []  # список дочерних узлов
        self.lvl = 0


class SimpleTree:
    def __init__(self, root):
        self.Root = root  # корень, может быть None
        self.__setNodeLvl__(root,1)

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


    def __getAllChild__(self,parentNode):
        nodes = [parentNode]
        if parentNode.Children.__len__() != 0:
            for node in parentNode.Children:
                nodes.append(self.__getAllChild__(node))
        return nodes

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

    def GetAllNodes(self):
        # ваш код выдачи всех узлов дерева в определённом порядке
        if self.Root is None:
            return []
        else:
            nodes = self.__getAllChild__(self.Root)
            while self.__countLists__(nodes) != 0:
                nodes = self.__makeOneList__(nodes)
            return nodes

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

    def Count(self):
        # количество всех узлов в дереве
        return self.GetAllNodes().__len__()

    def LeafCount(self):
        # количество листьев в дереве
        nodes = self.GetAllNodes()
        leavescnt = 0
        for node in nodes:
            if node.Children.__len__() == 0:
                leavescnt += 1
        return leavescnt
