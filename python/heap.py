'''
An unnecessarily complex implementation of a heap data structure.
'''

from .binary_tree import BinaryNode, BinaryTree
from operator import le, ge

def _comparisonFactory(comparisonFunction):
    def compareNodes(node1, node2):
        if node1 is None:
            return node2
        if node2 is None:
            return node1
        if comparisonFunction(node1.key, node2.key):
            return node1
        else:
            return node2
    return compareNodes

_max = _comparisonFactory(ge)
_min = _comparisonFactory(le)

def _swap(node1, node2):
    tree = node1.tree
    node1.index, node2.index = node2.index, node1.index
    tree._array[node1.index] = node1
    tree._array[node2.index] = node2


class HeapNode(BinaryNode):
    r'''A node of a heap tree.
    
    The node wraps a value (node.key) and has convenience methods
    for accessing node.left, node.right, and node.parent.
    '''

    def __init__(self, key = None, tree = None):
        self.index = None
        super().__init__(key = key, tree = tree)

    @property
    def left(self):
        if self.index is None:
            return None
        leftIndex = 2 * self.index
        if leftIndex <= len(self.tree):
            return self.tree[leftIndex]
        else:
            return None

    @left.setter
    def left(self, node): # Setters do not check to make sure node is a HeapNode
        if self.index is None:
            return None
        leftIndex = 2 * self.index
        if leftIndex <= len(self.tree):
            self.tree[leftIndex] = node
            node.index = leftIndex
            node.tree = self.tree
        else:
            raise IndexError('Node has no left child.')

    @property
    def right(self):
        if self.index is None:
            return None
        rightIndex = 2 * self.index + 1
        if rightIndex <= len(self.tree):
            return self.tree[rightIndex]
        else:
            return None

    @right.setter
    def right(self, node):
        if self.index is None:
            return None
        rightIndex = 2 * self.index + 1
        if rightIndex <= len(self.tree):
            self.tree[rightIndex] = node
            node.index = rightIndex
            node.tree = self.tree
        else:
            raise IndexError('Node has no right child.')

    @property
    def parent(self):
        if (self.index is not None) and (self.index != 1):
            return self.tree[self.index // 2]
        else:
            return None

    @parent.setter
    def parent(self, node):
        if (self.index is not None) and (self.index != 1):
            self.tree[self.index // 2] = node
            node.index = self.index // 2
            node.tree = self.tree
        else:
            return IndexError('Node is root of the tree and does not have parent.')

    def rotateLeft(self):
        raise NotImplementedError('HeapNode.rotateLeft')

    def rotateRight(self):
        raise NotImplementedError('HeapNode.rotateRight')

    def checkHeapProperty(self):
        assert self.tree.compare(self, self.left) is self, f"Subtree rooted at key = {self.key} is not a heap."
        assert self.tree.compare(self, self.right) is self, f"Subtree rooted at key = {self.key} is not a heap."
        if self.left is not None:
            assert self.tree is self.left.tree, f"Node (key = {self.key}) has a different tree attribute from its left child."
            self.left.checkHeapProperty()
        if self.right is not None:
            assert self.tree is self.right.tree, f"Node (key = {self.key}) has a different tree attribute from its right child."
            self.right.checkHeapProperty()
    
    def heapify(self):
        while True:
            moreHeapishChild = self.tree.compare(self.left, self.right)
            if moreHeapishChild is None:
                return
            moreHeapishNode = self.tree.compare(self, moreHeapishChild)
            if moreHeapishNode is moreHeapishChild:
                _swap(self, moreHeapishChild)
            else:
                return

    siftDown = heapify

    def siftUp(self):
        while True:
            if self.isRoot():
                return
            moreHeapishNode = self.tree.compare(self, self.parent)
            if moreHeapishNode is self:
                _swap(self, self.parent)
            else:
                return

    def delete(self):
        if self.tree is None:
            raise Exception('Node is not part of a heap.')
        lastNode = self.tree[-1]
        if self is lastNode:
            self.tree.pop()
            return self
        _swap(self, lastNode)
        self.tree.pop()
        if (lastNode.parent is None) or (lastNode.tree.compare(lastNode, lastNode.parent) is lastNode.parent):
            lastNode.siftDown()
        elif lastNode.tree.compare(lastNode, lastNode.parent) is lastNode:
            lastNode.siftUp()
        else:
            raise Exception('Unknown exception in HeapNode.delete()')
        return self


class Heap(BinaryTree):
    r'''Heap data structure

    Heap(type = 'max', fromList = None)
        
        Creates a heap from a list of values.

        Args:
            type (string): 'max' or 'min' for a max-heap or a min-heap, respectively
            fromList (list): iterable of objects that can be compared, or a list of BinaryNode objects   
        Example:
            >>> print(heap.Heap(fromList = range(10)))
                 ┌───9──┐  
              ┌──8──┐ ┌─6─┐
            ┌─7─┐ ┌─4 5   2
            0   3 1        
    '''
    
    def __init__(self, NodeType = HeapNode, type = 'max', fromList = None):
        # self._array = [None, None]
        self._array = []
        super().__init__(NodeType = NodeType)
        self.changeType(type, buildHeapFromList = fromList)

    def buildHeap(self, iterable):
        r'''Heap data structure

        Heap(type = 'max', fromList = None)
            
            Creates a heap from a list of values. If heap already contains nodes,
            extend the heap with new values from fromList.

            Args:
                type (string): 'max' or 'min' for a max-heap or a min-heap, respectively.
                fromList (list): iterable of objects that can be compared, or a list of BinaryNode objects.
        '''
        # if iterable is None:
        #     raise IndexError('Passed None to Heap.buildHeap')
        # self._array.pop()
        current_index = len(self._array)
        for elem in iterable:
            node = HeapNode(elem) # Doesn't check for invalid elem
            node.index = current_index
            node.tree = self
            self._array.append(node) # Doesn't check if node is already in self._array
            current_index += 1
        for idx in range(len(self) // 2, 0, -1):
            self._array[idx].heapify()

    extend = buildHeap
    
    def __len__(self):
        return len(self._array) - 1

    def __getitem__(self, index):
        return self._array[index]

    def __setitem__(self, index, value):
        self._array[index] = value

    @property
    def root(self):
        if len(self) < 1:
            return None
        return self._array[1]

    @root.setter
    def root(self, node): # Maybe should forbid appending None to self._array...
        if len(self._array) == 0:
            self._array.append(None)
        elif len(self._array) == 1:
            self._array.append(node)
            node.tree = self
        else:
            self._array[1] = node
            node.tree = self

    def checkHeapProperty(self):
        '''Check that the rep invariant of the heap is preserved by
        recursively checking the left and right children of each node.'''
        self.root.checkHeapProperty()

    def changeType(self, type, buildHeapFromList = None):
        '''Change the heap type from a max-heap to a min-heap or vice-versa.
        
        self.changeType(type, buildHeapFromList = None)
        
            Args:
                type (string): 'max' or 'min' for a max-heap or a min-heap, respectively.
                buildHeapfromList (list): iterable of objects that can be compared, or a list
                    of BinaryNode objects. After changing the heap type, the heap is extended
                    by adding values from buildHeapFromList.
        '''
        if buildHeapFromList is None:
            buildHeapFromList = []
        if type.lower() == 'max':
            self.compare = _max
        elif type.lower() == 'min':
            self.compare = _min
        else:
            raise Exception(f'Unknown comparison type {type} in Heap.changeType(type)')
        self.type = type
        self.buildHeap(buildHeapFromList)

    def peek(self):
        '''Peek at the root node'''
        return self.root

    def pop(self):
        if len(self._array) <= 1:
            return None
        lastNode = self._array.pop()
        lastNode.tree = None
        return lastNode

    def extract(self):
        '''Extract the root node'''
        if len(self) < 1:
            return None
        _swap(self._array[1], self._array[-1])
        extractedNode = self.pop()
        if len(self) > 0:
            self._array[1].heapify()
        return extractedNode

    def sortedList_(self):
        r'''Empties the heap and returns a sorted list of HeapNode objects.

            Args: N/A
            Return:
                List of HeapNode objects, sorted from least to greatest if min-heap and
                greatest to least if max-heap.
            Example:
                >>> [node.key for node in heap.Heap(fromList = range(10)).sortedList_()]
                [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        '''
        nodeList = []
        current = self.extract()
        while current is not None:
            nodeList.append(current)
            current = self.extract()
        return nodeList

    def insert(self, key):
        if key is None:
            return None
        newNode = self.NodeType(key)
        newNode.tree = self
        newNode.index = len(self) + 1
        self._array.append(newNode)
        newNode.siftUp()
        return newNode