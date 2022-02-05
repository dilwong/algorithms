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