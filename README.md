# algorithms

Implementing standard, well-known algorithms to make sure I actually understand them...

For example, an AVL tree:

```
import random

from algorithms import AVL
AVLTree = AVL.AVLTree

random.seed(137)
randomList = [random.randint(0, 100) for _ in range(25)]
myTree = AVLTree(fromList = randomList)
print(myTree)
```

Outputs:

```
            ┌─────────44────────────────┐             
     ┌─────24────┐             ┌───────65────────┐    
  ┌──9────┐   ┌─41─┐        ┌─52────┐        ┌──78─┐  
┌─1─┐  ┌─23  29   41─┐   ┌─51    ┌─60─┐   ┌─66─┐  85─┐
0   3 17            42  50      54   62  66   67    88
```

Or display the tree horizontally with `print(f'{myTree:h}')`:

```
root: 44
├── left: 24
│   ├── left: 9
│   │   ├── left: 1
│   │   │   ├── left: 0
│   │   │   └── right: 3
│   │   └── right: 23
│   │       └── left: 17
│   └── right: 41
│       ├── left: 29
│       └── right: 41
│           └── right: 42
└── right: 65
    ├── left: 52
    │   ├── left: 51
    │   │   └── left: 50
    │   └── right: 60
    │       ├── left: 54
    │       └── right: 62
    └── right: 78
        ├── left: 66
        │   ├── left: 66
        │   └── right: 67
        └── right: 85
            └── right: 88
```

And here's a max-heap:

```
maxHeap = heap.Heap(fromList = randomList)
print(maxHeap)
```

Output:

```
                ┌────────────────88────────────┐       
        ┌──────78────────┐                 ┌──85────┐  
    ┌──66───┐        ┌──65────┐        ┌──52─┐   ┌─67─┐
 ┌─54─┐  ┌─66─┐   ┌─51─┐   ┌─24─┐   ┌─41─┐  50  62   60
17   44  1   41  42    0  23    3  29    9             
```
And change to min-heap using `maxHeap.changeType('min')`.