# AAVL Tree in Python

his project is a full implementation of an **AVL Tree** in Python, developed as part of a university Data Structures course. The tree supports dynamic insertions, deletions, and searches while maintaining balance for guaranteed logarithmic time complexity.

## Features

- Self-balancing binary search tree
- Insert, delete, and search operations
- Finger search optimization
- Join and split tree functionality
- Successor search and in-order traversal
- Node height and balance management

##Rotations and Rebalancing

- The tree automatically maintains balance using **left** and **right rotations**.
- The `rebalance()` method is called after insertions or deletions.
- Rotations occur in constant time `O(1)`; rebalancing is `O(log n)` in the worst case.

## ⏱️ Time Complexities

| Operation        | Complexity |
|------------------|------------|
| insert           | O(log n)   |
| delete           | O(log n)   |
| search           | O(log n)   |
| join             | O(log n) + O(log m) |
| split            | O(log n)   |
| avl_to_array     | O(n)       |
| get_root / size  | O(1)       |

---

##  Design Notes

- Uses **virtual nodes** (with height -1) to simplify edge-case handling.
- `finger_insert()` and `finger_search()` are optimized variants that start from the max node.
- `join()` and `split()` operations enable building larger trees or dividing them efficiently.

---
##  Experimental Insights

- Performance was tested on sorted, reversed, and randomized sequences.
- Results show that:
  - Rebalancing cost grows linearly with input size → **O(n)** total cost.
  - Rotations are required more frequently in sorted or reverse-sorted input, due to skewed growth.
  - The ratio between theoretical and experimental search costs remained consistent across all test types.
- These findings validate the theoretical guarantees of the AVL tree structure.

---

##  Structure

- `AVLTree.py` – AVL Tree implementation and all public operations
- `AVLNode` – Inner class representing nodes in the tree


## Technologies

- Language: Python 3
- IDE: PyCharm
- OOP-based structure with class design

## Author

Yoav Ben Guigui  
B.Sc. Mathematics & Computer Science, Tel Aviv University
