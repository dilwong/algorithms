from .binary_tree import BinaryNode, BinaryTree

class BinarySearchNode(BinaryNode):
    
    def __init__(self, key = None, left = None, right = None, parent = None):
        super().__init__(key = key, left = left, right = right, parent = parent)
    
    def find(self, value):
        """Find a node with a key = value in the subtree rooted at this node."""
        if self.key == value:
            return self
        elif value < self.key:
            if self.left is not None:
                return self.left.find(value)
            else:
                return None
        elif self.key < value:
            if self.right is not None:
                return self.right.find(value)
            else:
                return None
    
    def minimum(self):
        """Find the node with the smallest key in the subtree rooted at this node."""
        current_node = self
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def maximum(self):
        """Find the node with the largest key in the subtree rooted at this node."""
        current_node = self
        while current_node.right is not None:
            current_node = current_node.right
        return current_node
    
    def successor(self):
        """In the containing binary search tree, find the node with the smallest key larger than (or equal to) that of this node."""
        if self.right is not None:
            return self.right.minimum()
        else:
            current = self
            while not current.isLeftChild():
                current = current.parent
                if current is None:
                    return None
            return current.parent

    def predecessor(self):
        """In the containing binary search tree, find the node with the largest key smaller than (or equal to) that of this node."""
        if self.left is not None:
            return self.left.maximum()
        else:
            current = self
            while not current.isRightChild():
                current = current.parent
                if current is None:
                    return
            return current.parent

    def insert(self, node):
        """Insert node into the subtree rooted at this node. You can violate the BST property by calling this method directly."""
        if node is None:
            return
        if node.key <= self.key:
            if self.left is None:
                node.parent = self
                node.tree = self.tree # Note that this does not recursively set tree in the subnodes of node
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                node.parent = self
                node.tree = self.tree # Note that this does not recursively set tree in the subnodes of node
                self.right = node
            else:
                self.right.insert(node)
    
    def delete(self):
        """Delete this node from the containing binary search tree, and return this node."""
        if (self.left is None) or (self.right is None):
            parent = self.parent
            if self.isLeftChild():
                parent.left = self.left or self.right
                if parent.left is not None:
                    parent.left.parent = parent
            elif self.isRightChild():
                parent.right = self.left or self.right
                if parent.right is not None:
                    parent.right.parent = parent
            elif parent is None:
                tree = self.tree
                tree.root = self.left or self.right
                if tree.root is not None:
                    tree.root.parent = None
            return self
        else:
            successor = self.successor()
            self.key, successor.key = successor.key, self.key
            return successor.delete()


class BinarySearchTree(BinaryTree):

    def __init__(self, NodeType = BinarySearchNode, fromList = None):
        super().__init__(NodeType = NodeType)
        if fromList is not None:
            self.extend(fromList)
    
    def find(self, value):
        return self.root and self.root.find(value)

    def minimum(self):
        return self.root and self.root.minimum()

    def maximum(self):
        return self.root and self.root.maximum()

    def insert(self, key):
        if key is None:
            return None
        newNode = self.NodeType(key)
        newNode.tree = self
        newNode.left = None
        newNode.right = None
        if self.root is None:
            newNode.parent = None
            self.root = newNode
        else:
            self.root.insert(newNode)
        return newNode
    
    def extend(self, iterable):
        for elem in iterable:
            self.insert(elem)
    
    def delete(self, value):
        """Delete a node with key = value in this BST. Does not delete duplicates."""
        node = self.find(value)
        if node is None:
            return None
        return node.delete()

    def successor(self, value):
        node = self.find(value)
        if node is None:
            return None
        current = node
        while current.key == node.key:
            current = current.successor()
        return current

    def sortedList(self): # Also same as inOrderTraversal
        nodeList = []
        current = self.minimum()
        while current is not None:
            nodeList.append(current)
            current = current.successor()
        return nodeList

    def reverseSortedList(self): # Should be same as list(reversed(sortedList()))
        nodeList = []
        current = self.maximum()
        while current is not None:
            nodeList.append(current)
            current = current.predecessor()
        return nodeList