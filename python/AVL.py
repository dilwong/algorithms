from .BST import BinarySearchNode, BinarySearchTree

class AVLNode(BinarySearchNode):

    def height(self):
        try:
            return self._height
        except AttributeError:
            self._height = super().height()
            return self._height
    
    def fix_height(self):
        if self.left is None:
            leftHeight = -1
        else:
            leftHeight = self.left.height()
        if self.right is None:
            rightHeight = -1
        else:
            rightHeight = self.right.height()
        self._height = 1 + max(leftHeight, rightHeight)

    def fix_avl_property(self):
        self.fix_height()
        leftHeight = self.left.height() if self.left else -1
        rightHeight = self.right.height() if self.right else -1
        if leftHeight > rightHeight + 1:
            leftLeftHeight = self.left.left.height() if self.left.left else -1
            leftRightHeight = self.left.right.height() if self.left.right else -1
            if leftRightHeight > leftLeftHeight:
                self.left.rotateLeft()
            self.rotateRight()
        elif rightHeight > leftHeight + 1:
            rightRightHeight = self.right.right.height() if self.right.right else -1
            rightLeftHeight = self.right.left.height() if self.right.left else -1
            if rightLeftHeight > rightRightHeight:
                self.right.rotateRight()
            self.rotateLeft()
        if self.parent is not None:
            self.parent.fix_avl_property()
    
    def rotateRight(self):
        super().rotateRight()
        self.fix_height()
        self.parent.fix_height()

    def rotateLeft(self):
        super().rotateLeft()
        self.fix_height()
        self.parent.fix_height()

    def insert(self, node, fix_avl = False):
        super().insert(node)
        if fix_avl:
            node.fix_avl_property()
    
    def delete(self, fix_avl = False):
        node = super().delete()
        if fix_avl:
            self.parent.fix_avl_property()
        return node

class AVLTree(BinarySearchTree):

    def __init__(self, NodeType = AVLNode, fromList = None):
        super().__init__(NodeType = NodeType, fromList = fromList)

    def insert(self, key):
        node = super().insert(key)
        if node is not None:
            node.fix_avl_property()
        return node

    def delete(self, value):
        node = super().delete(value)
        if (node is not None) and (node.parent is not None):
            node.parent.fix_avl_property()
        return node