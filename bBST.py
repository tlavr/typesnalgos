class BSTNode:
    def __init__(self, key, parent):
        self.NodeKey = key  # ключ узла
        self.Parent = parent  # родитель или None для корня
        self.LeftChild = None  # левый потомок
        self.RightChild = None  # правый потомок
        self.Level = 0  # уровень узла


class BalancedBST:
    def __init__(self):
        self.Root = None  # корень дерева
        self.allNodes = []

    def makeTree(self, nodeParent, arr, lvl):
        if arr.__len__() > 0:
            centIdx = round(arr.__len__() / 2 - 0.1)
            node = BSTNode(None, None)
            node.NodeKey = arr[centIdx]
            node.Parent = nodeParent
            node.Level = lvl
            node.LeftChild = self.makeTree(node, arr[:centIdx], lvl+1)
            node.RightChild = self.makeTree(node, arr[centIdx + 1:], lvl+1)
            return node
        return None

    def GenerateTree(self, a):
    # создаём дерево с нуля из неотсортированного массива a
        if a.__len__() == 0:
            return None
        # Sort array
        a = sorted(a)
        # Recursive add all elements
        self.Root = self.makeTree(None, a, 1)  # parameters for the first adding

    def detTreeLvl(self, node, lvl):
        if node.Level > lvl:
            lvl = node.Level
        if node.LeftChild is not None:
            lvl = self.detTreeLvl(node.LeftChild,lvl)
        if node.RightChild is not None:
            lvl = self.detTreeLvl(node.RightChild,lvl)
        return lvl

    def IsBalanced(self, root_node):
        if root_node is not None:
            if root_node.LeftChild is not None:
                if root_node.RightChild is not None:
                    if abs(self.detTreeLvl(root_node.LeftChild,root_node.Level)-self.detTreeLvl(root_node.RightChild,root_node.Level)) < 2:
                        return True
                else:
                    if abs(self.detTreeLvl(root_node.LeftChild,root_node.Level) - root_node.Level) < 2:
                        return True
            else:
                if root_node.RightChild is not None:
                    if abs(self.detTreeLvl(root_node.RightChild,root_node.Level) - root_node.Level) < 2:
                        return True
                else:
                    return True
        return False  # сбалансировано ли дерево с корнем root_node

    def __collectAllNodes__(self,fromNode = None, mode = 0):
        if fromNode is None or fromNode is self.Root:
            fromNode = self.Root
            self.allNodes = []
        if fromNode is None:
            return
        if mode == 2:
            self.allNodes.append(fromNode)
        if fromNode.LeftChild is not None:
            self.__collectAllNodes__(fromNode.LeftChild)
        if mode == 0:
            self.allNodes.append(fromNode)
        if fromNode.RightChild is not None:
            self.__collectAllNodes__(fromNode.RightChild)
        if mode == 1:
            self.allNodes.append(fromNode)

    def getAllNodes(self):
        self.__collectAllNodes__()
        return self.allNodes