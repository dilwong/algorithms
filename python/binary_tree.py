class StringList(list):
    
    def __init__(self, val, nodePosition, stringLength):
        super().__init__(val)
        self.nodePosition = nodePosition
        self.stringLength = stringLength


class BinaryNode:
    
    def __new__(cls, *args, **kwargs):
        if len(args) > 0:
            key = args[0]
        elif 'key' in kwargs:
            key = kwargs['key']
        else:
            key = None
        if isinstance(key, BinaryNode):
            return key
        else:
            return super().__new__(cls)
    
    def __init__(self, key = None, left = None, right = None, parent = None, tree = None):
        self.left = left
        self.right = right
        
        self.parent = parent
        self.key = key
        
        self.tree = tree
    
    def isLeftChild(self):
        if self.parent is not None:
            return self.parent.left is self
        else:
            return False
    
    def isRightChild(self):
        if self.parent is not None:
            return self.parent.right is self
        else:
            return False

    def height(self):
        """Height of the subtree rooted at this node."""
        if (self.left is None) and (self.right is None):
            return 0
        else:
            if self.left is None:
                return 1 + self.right.height()
            if self.right is None:
                return 1 + self.left.height()
            return 1 + max(self.left.height(), self.right.height())

    def depth(self):
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.depth()

    def inOrderTraversal(self):
        travelList = []
        if self is not None:
            if self.left is not None:
                travelList.extend(self.left.inOrderTraversal())
            travelList.append(self)
            if self.right is not None:
                travelList.extend(self.right.inOrderTraversal())
        return travelList

    def preOrderTraversal(self):
        travelList = []
        if self is not None:
            travelList.append(self)
            if self.left is not None:
                travelList.extend(self.left.preOrderTraversal())
            if self.right is not None:
                travelList.extend(self.right.preOrderTraversal())
        return travelList
    
    def postOrderTraversal(self):
        travelList = []
        if self is not None:
            if self.left is not None:
                travelList.extend(self.left.postOrderTraversal())
            if self.right is not None:
                travelList.extend(self.right.postOrderTraversal())
            travelList.append(self)
        return travelList

    def levelOrderTraversal(self):
        """Breadth-First-Search Ordering"""
        from collections import deque
        travelList = []
        queue = deque([[self]])
        while queue:
            path = queue.popleft()
            travelList.append(path[-1])
            if path[-1].left is not None:
                queue.append(path + [path[-1].left])
            if path[-1].right is not None:
                queue.append(path + [path[-1].right])
        return travelList

    def rotateRight(self):
        if self.left is None:
            raise Exception(f'Node with key = {self.key} cannot rotateRight because it has no left child.')
        newRoot = self.left
        parent = self.parent
        newRoot.parent = parent
        if parent is None:
            self.tree.root = newRoot
        else:
            if self.isRightChild():
                parent.right = newRoot
            else: # if self.isLeftChild()
                parent.left = newRoot
        self.left = newRoot.right
        if self.left is not None:
            self.left.parent = self
        newRoot.right = self
        self.parent = newRoot

    def rotateLeft(self):
        if self.right is None:
            raise Exception(f'Node with key = {self.key} cannot rotateLeft because it has no right child.')
        newRoot = self.right
        parent = self.parent
        newRoot.parent = parent
        if parent is None:
            self.tree.root = newRoot
        else:
            if self.isRightChild():
                parent.right = newRoot
            elif self.isLeftChild():
                parent.left = newRoot
        self.right = newRoot.left
        if self.right is not None:
            self.right.parent = self
        newRoot.left = self
        self.parent = newRoot

    def nthParent(self, n): # n = 0 is self, n = 1 is parent, n = 2 is grandparent, n = 3 is great-grandparent
        if n < 0:
            return None
        current = self
        for _ in range(n):
            if current.parent is None:
                return None
            current = current.parent
        return current

    def nthDescendents(self, n):
        if n < 1:
            return []
        if n == 1:
            return [node for node in self.children() if node is not None]
        if self.left is None:
            leftDescendents = []
        else:
            leftDescendents = self.left.nthDescendents(n - 1)
        if self.right is None:
            rightDescendents = []
        else:
            rightDescendents = self.right.nthDescendents(n - 1)
        leftDescendents.extend(rightDescendents)
        return leftDescendents

    def children(self):
        return (self.left, self.right)

    def sibling(self):
        if self.parent is None:
            return None
        if self.isLeftChild():
            return self.parent.right
        else: # if self.isRightChild()
            return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

    def nthLevelCousins(self, n):
        try:
            nodeSibling = self.sibling()
            return [node for node in self.nthParent(n).nthDescendents(n) if (node is not self) and (node is not nodeSibling)]
        except AttributeError:
            return []

    def _print_key(self):
        keyString = str(self.key)
        if isinstance(self.key, (int, float)) and self.key < 0:
            keyString = ' ' + keyString + ' '
        return keyString

    def _str_lists(self):
        if (self.left is None) and (self.right is None):
            keyString = self._print_key()
            return StringList([keyString], len(keyString) // 2, len(keyString))
        if self.left is None:
            leftStringList = StringList([], 0, 0)
            topLeftString = ''
            leftStringLength = 0
        else:
            leftStringList = self.left._str_lists()
            topLeftString = (' ' * leftStringList.nodePosition) + '┌─'
            topLeftString += '─' * max(leftStringList.stringLength - len(topLeftString), 0)
            leftStringLength = len(topLeftString)
            padLength = leftStringLength - leftStringList.stringLength
            if padLength > 0:
                for idx in range(len(leftStringList)):
                    leftStringList[idx] = leftStringList[idx] + (' ' * padLength)
        if self.right is None:
            rightStringList = StringList([], 0, 0)
            topRightString = ''
            rightStringLength = 0
        else:
            rightStringList = self.right._str_lists()
            topRightString = '─┐' + (' ' * (rightStringList.stringLength - 1 - rightStringList.nodePosition))
            topRightString = ('─' * max(rightStringList.stringLength - len(topRightString), 0)) + topRightString
            rightStringLength = len(topRightString)
            padLength = rightStringLength - rightStringList.stringLength
            if padLength > 0:
                for idx in range(len(rightStringList)):
                    rightStringList[idx] = (' ' * padLength) + rightStringList[idx]
        while len(rightStringList) > len(leftStringList):
            leftStringList.append(' ' * leftStringLength)
        while len(leftStringList) > len(rightStringList):
            rightStringList.append(' ' * rightStringLength)
        keyString = self._print_key()
        # dashes = 2 * '─'
        dashes = ''
        keyLeftPad = '' if self.left is None else dashes
        keyRightPad = '' if self.right is None else dashes
        topString = topLeftString + keyLeftPad + keyString + keyRightPad + topRightString
        middlePadLength = len(keyLeftPad) + len(keyString) + len(keyRightPad)
        newStringList = StringList([], leftStringLength + len(keyLeftPad) + len(keyString) // 2, len(topString))
        newStringList.append(topString)
        for idx in range(len(leftStringList)):
            newStringList.append(leftStringList[idx] + (' ' * middlePadLength) + rightStringList[idx])
        return newStringList
    
    def __str__(self):
        return f'{self:v}'

    def _horizontal_str(self, subtree_strings = [], spine = ''):
        if self.parent is None:
            prefix = 'root: '
            addendum = ''
        elif self.isLeftChild():
            prefix = 'left: '
            if self.sibling() is not None:
                prefix = '├── ' + prefix
                addendum = '│   '
            else:
                prefix = '└── ' + prefix
                addendum = '    '
        else: # if self.isRightChild()
            prefix = '└── right: '
            addendum = '    '
        subtree_strings.extend((spine, prefix, str(self.key),'\n'))
        if self.left is not None:
            self.left._horizontal_str(subtree_strings, spine + addendum)
        if self.right is not None:
            self.right._horizontal_str(subtree_strings, spine + addendum)
        return subtree_strings

    def __format__(self, spec):
        if spec.lower()[0] == 'v':
            strlist = self._str_lists()
            return '\n'.join(strlist)
        elif spec.lower()[0] == 'h':
            strlist = self._horizontal_str()
            return ''.join(strlist)
        else:
            raise TypeError('Unsupported format string passed to ' + self.__class__.__name__ + '.__format__')
    
    def __repr__(self):
        return super().__repr__() + f' (key = {self.key})'


class BinaryTree:
    
    def __init__(self, NodeType = BinaryNode):
        self.NodeType = NodeType
        self.root = None

    def __format__(self, spec):
        if spec.lower()[0] == 'v':
            return f'{self.root:v}'
        elif spec.lower()[0] == 'h':
            return f'{self.root:h}'
        else:
            raise TypeError('Unsupported format string passed to ' + self.__class__.__name__ + '.__format__')
    
    def __str__(self):
        if self.root is None:
            return None.__str__()
        return f'{self:v}'

    def height(self):
        if self.root is None:
            return None
        else:
            return self.root.height()

    def nodeAtIndex(self, index):
        """Find the node at index, indexing the root at 1"""
        if index < 1:
            return None
        binaryIndex = f"{index:b}"[1:]
        current = self.root
        for idx in binaryIndex:
            if current is None:
                break
            if idx == '0':
                current = current.left
            elif idx == '1':
                current = current.right
        else:
            return current
        return None

    def inOrderTraversal(self):
        if self.root is not None:
            return self.root.inOrderTraversal()

    def preOrderTraversal(self):
        if self.root is not None:
            return self.root.preOrderTraversal()
    
    def postOrderTraversal(self):
        if self.root is not None:
            return self.root.postOrderTraversal()

    def levelOrderTraversal(self):
        if self.root is not None:
            return self.root.levelOrderTraversal()


def subtreesEqual(node1, node2):
    """Are subtrees rooted at node1 and node2 identical?"""
    if (node1 is None) and (node2 is None):
        return True
    if (node1 is not None) and (node2 is not None):
        if node1.key != node2.key:
            return False
        return subtreesEqual(node1.left, node2.left) and subtreesEqual(node1.right, node2.right)
    return False