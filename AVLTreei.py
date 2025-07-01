# id: 206570707
# name: Yoav Ben Guigui
# username1:benguigui1


"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value, is_virtual=False):
        self.key = key
        self.value = value
        if is_virtual:
            self.left = None
            self.right = None
            self.parent = None
            self.height = -1
        else:
            self.left = VirtualNode
            self.right = VirtualNode
            self.parent = VirtualNode
            self.height = 0

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.height != -1


VirtualNode = AVLNode(None, None, is_virtual=True)

"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.root = VirtualNode
        self.tree_size = 0

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key):
        x = self.root
        count = 0
        while x.is_real_node():
            if key == x.key:
                return x, count + 1
            if key < x.key:
                count += 1
                x = x.left
            else:
                count += 1
                x = x.right
        return None, count + 1

    """searches for a node in the dictionary corresponding to the key (starting at the max)

        @type key: int
        @param key: a key to be searched
        @rtype: (AVLNode,int)
        @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
        and e is the number of edges on the path between the starting node and ending node+1.
        """

    def finger_search(self, key):
        current = self.max_node()
        count = 0
        while current.parent.is_real_node() and key < current.key and key < current.parent.key:
            current = current.parent
            count += 1
        if current.key == key:
            return current, count + 1
        if key < current.key:
            while current.is_real_node():
                if current.key == key:
                    return current, count + 1
                elif current.key > key:
                    current = current.left
                    count += 1
                elif current.key < key:
                    current = current.right
                    count += 1
        return None, count

    """
        Performs a right rotation around a given node.
        @type node: AVLNode
    """
    # 
    def _rotate_right(self, node):
        y = node.left
        node.left = y.right
        if y.right.is_real_node():
            y.right.parent = node
        y.parent = node.parent
        if not node.parent.is_real_node():
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.right = node
        node.parent = y
        self._update_height(node)
        self._update_height(y)

    """
        Performs a left rotation around a given node.
        @type node: AVLNode
    """

    def _rotate_left(self, node):
        y = node.right
        node.right = y.left
        if y.left.is_real_node():
            y.left.parent = node
        y.parent = node.parent
        if not node.parent.is_real_node():
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y
        self._update_height(node)
        self._update_height(y)

    """
        Calculates the balance factor of a node.
        @type node: AVLNode
        @rtype: int
        @returns: the balance factor (left_height - right_height).
    """

    def _get_balance(self, node):
        left_height = node.left.height
        right_height = node.right.height
        return left_height - right_height

    """
        Updates the height of a node based on its children's heights.
        @type node: AVLNode
    """

    def _update_height(self, node):
        left_height = node.left.height
        right_height = node.right.height
        node.height = max(left_height, right_height) + 1

    """
        Rebalances the tree starting from a given node and propagates upwards.
        @type node: AVLNode
        @rtype: int
        @returns: the number of promote operations performed.
    """

    def _rebalance(self, node):
        promote_count = 0
        current = node
        while current.is_real_node():
            old_height = current.height
            self._update_height(current)
            new_height = current.height
            if new_height != old_height and abs(
                    self._get_balance(current)) < 2:  # balanced but height has changed so promote
                promote_count += 1
            balance = self._get_balance(current)
            if balance > 1:  # Left-heavy
                if self._get_balance(current.left) < 0:  # Left-Right case
                    self._rotate_left(current.left)
                self._rotate_right(current)
            elif balance < -1:  # Right-heavy
                if self._get_balance(current.right) > 0:  # Right-Left case
                    self._rotate_right(current.right)
                self._rotate_left(current)

            current = current.parent

        return promote_count

    """
        Inserts a new node into the AVL tree with the given key and value.
        @type key: int
        @type val: string
        @rtype: (AVLNode, int, int)
        @returns: a tuple (x, e, h) where:
        x is the new node,
        e is the number of edges from the root to the new node,
        h is the number of promote operations performed.
    """

    def insert(self, key, val):
        if not self.root.is_real_node():  # if tree is empty
            new_node = AVLNode(key, val)
            self.root = new_node
            self.tree_size += 1
            return new_node, 0, 0

        current = self.root
        parent = None
        edge_count = 0
        # look for the right place for the new node
        while current.is_real_node():
            parent = current
            edge_count += 1
            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = AVLNode(key, val)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self.tree_size += 1
        promote_count = self._rebalance(parent)  # rebalance the tree
        return new_node, edge_count, promote_count

    """
        Inserts a new node into the AVL tree with the given key and value starting from the max.
        @type key: int
        @type val: string
        @rtype: (AVLNode, int, int)
        @returns: a tuple (x, e, h) where:
        x is the new node,
        e is the number of edges from the max node to the new node,
        h is the number of promote operations performed.
    """

    def finger_insert(self, key, val):
        if not self.root.is_real_node():  # if tree is empty
            new_node = AVLNode(key, val)
            self.root = new_node
            self.tree_size += 1
            return new_node, 0, 0
        num_edges = 0
        current = self.max_node()
        if key > current.key:
            new_node = AVLNode(key, val)
            new_node.parent = current
            current.right = new_node
            num_edges = 1
        else:
            # Climb up the right "spine"
            while current.parent.is_real_node() and key < current.parent.key:
                current = current.parent
                num_edges += 1
            parent = None
            # Do a regular insertion from here (first step will be to go left)
            while current.is_real_node():
                parent = current
                num_edges += 1
                if key < current.key:
                    current = current.left
                else:
                    current = current.right

            new_node = AVLNode(key, val)
            new_node.parent = parent
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node

        self.tree_size += 1
        promote_count = self._rebalance(new_node.parent)

        return new_node, num_edges, promote_count

    """
        Replaces the old_node with new_node in the AVL tree.
        @type old_node: AVLNode
        @type new_node: AVLNode
    """

    def _replace_node(self, old_node, new_node):
        parent = old_node.parent
        if parent.is_real_node():
            if parent.left == old_node:
                parent.left = new_node
            else:
                parent.right = new_node
        else:
            self.root = new_node
        if new_node:
            new_node.parent = parent

    """
        Deletes a node from the dictionary.
        @type node: AVLNode
        @pre: node is a real pointer to a node in self.
    """

    def delete(self, node):
        if not node.is_real_node():
            return
        # Step 1: Handle cases of node deletion
        parent = node.parent
        left_child_real = node.left.is_real_node()
        right_child_real = node.right.is_real_node()

        if not left_child_real and not right_child_real:
            # Case 1: Leaf node
            if parent:
                if parent.left == node:
                    parent.left = None
                else:
                    parent.right = None
            else:
                self.root = None
        elif left_child_real and not right_child_real:
            # Case 2: One child (left)
            child = node.left
            self._replace_node(node, child)
        elif not left_child_real and right_child_real:
            # Case 2: One child (right)
            child = node.right
            self._replace_node(node, child)
        else:
            # Case 3: Two children
            successor = self.successor(node)
            node.key = successor.key
            node.value = successor.value
            self.delete(successor)

        # Step 2: Rebalance the tree
        if parent.is_real_node():
            self._rebalance(parent)
        else:
            if self.root:
                self._rebalance(self.root)

    """
        Joins self with item and another AVLTree.
        @type tree2: AVLTree
        @param tree2: a dictionary to be joined with self
        @type key: int
        @param key: the key separating self and tree2
        @type val: string
        @param val: the value corresponding to key
        @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
                   or the opposite way.
    """

    def join(self, t, k, v):
        if not self.root.is_real_node():
            t.insert(k, v)
            self.root = t.root
            self.tree_size = t.tree_size
            return
        if not t.root.is_real_node():
            self.insert(k, v)
            return
        if (self.root.key < k) and (t.root.key > k):
            smaller_tree = self
            larger_tree = t
        else:
            smaller_tree = t
            larger_tree = self
        h1 = smaller_tree.root.height
        h2 = larger_tree.root.height
        if h1 < h2 or h1 == h2:
            current = larger_tree.root
            while current.left.is_real_node() and current.left.height > h1:
                current = current.left

            new_node = AVLNode(k, v)
            new_node.left = smaller_tree.root
            if new_node.left.is_real_node():
                new_node.left.parent = new_node
            new_node.right = current.left
            if new_node.right.is_real_node():
                new_node.right.parent = new_node
            current.left = new_node
            new_node.parent = current
        else:
            current = smaller_tree.root
            while current.right.is_real_node() and current.get_right().get_height() > h2:
                current = current.get_right()

            new_node = AVLNode(k, v)
            new_node.right = larger_tree.root
            if new_node.right.is_real_node():
                new_node.right.parent = new_node
            new_node.left = current.right
            if new_node.left.is_real_node():
                new_node.left.parent = new_node
            current.right = new_node
            new_node.parent = current

        # Rebalance the tree
        if h1 < h2 or h1 == h2:
            larger_tree._rebalance(larger_tree.root)
            self.root = larger_tree.root
            self.tree_size += smaller_tree.tree_size + 1
        else:
            smaller_tree._rebalance(smaller_tree.root)
            self.root = smaller_tree.root
            self.tree_size += larger_tree.tree_size + 1

    """
        Joins two AVL trees with a given key and value into a single AVL tree.
        @type key: int
        @type value: string
        @type left_tree: AVLTree
        @type right_tree: AVLTree
        @rtype: AVLTree
        @returns: A new AVLTree that combines left_tree and right_tree with the key and value.
    """

    def _join_trees(self, key, value, left_tree, right_tree):
        new_tree = AVLTree()
        new_node = AVLNode(key, value)

        new_node.left = left_tree.root
        if new_node.left.is_real_node():
            new_node.left.parent = new_node

        new_node.right = right_tree.root
        if new_node.right.is_real_node():
            new_node.right.parent = new_node

        new_tree.root = new_node
        new_tree._rebalance(new_node)

        return new_tree

    """
        Splits the dictionary at a given node.
        @type x: AVLNode
        @pre: x is in self
        @param x: the node in the dictionary to be used for the split
        @rtype: (AVLTree, AVLTree)
        @returns: a tuple (t1, t2), where t1 is an AVLTree representing the keys smaller than x,
                      and t2 is an AVLTree representing the keys larger than x.
    """

    def split(self, x):
        if x.is_real_node():
            return AVLTree(), AVLTree()

        t1 = AVLTree()
        t2 = AVLTree()
        if x.left.is_real_node():
            t1.root = x.left
            t1.root.parent = None
        if x.right.is_real_node():
            t2.root = x.right
            t2.root.parent = None

        current = x.parent
        while current.is_real_node():
            if current.left == x:
                new_tree = AVLTree()
                if current.right.is_real_node():
                    new_tree.root = current.right
                    new_tree.root.parent = None
                t2 = self._join_trees(current.key, current.value, new_tree, t2)
            else:
                new_tree = AVLTree()
                if current.left.is_real_node():
                    new_tree.root = current.left
                    new_tree.root.parent = None
                t1 = self._join_trees(current.key, current.value, t1, new_tree)

            x = current
            current = current.parent

        return t1, t2

    """
        Returns an array representing dictionary.
        @rtype: list
        @returns: a sorted list according to key of tuples (key, value) representing the data structure.
    """

    def avl_to_array(self):
        if not self.root.is_real_node():
            return []

        min_node = self.root
        while min_node.left.is_real_node():
            min_node = min_node.left

        key_arr = []
        while min_node.is_real_node():
            key_arr.append((min_node.key, min_node.value))
            min_node = self.successor(min_node)
        return key_arr

    """
        Returns the node with the maximal key in the dictionary.
        @rtype: AVLNode
        @returns: the maximal node, None if the dictionary is empty.
    """

    def max_node(self):
        x = self.root
        if not x.is_real_node():
            return None
        while x.right.is_real_node():  # go to the rightmost node
            x = x.right
        return x

    """
        Returns the number of items in the dictionary.
        @rtype: int
        @returns: the number of items in the dictionary.
    """

    def size(self):
        return self.tree_size

    """
        Returns the root of the tree representing the dictionary.
        @rtype: AVLNode
        @returns: the root, None if the dictionary is empty.
    """

    def get_root(self):
        return self.root

    """
        Finds the successor of a given node.
        @type node: AVLNode
        @rtype: AVLNode
        @returns: the successor node, or None if there is no successor.
    """

    def successor(self, node):
        if not node.is_real_node():
            return None

        right_child = node.right
        if right_child.is_real_node():
            node = right_child
            while node.left.is_real_node():
                node = node.left
            return node

        parent = node.parent
        while parent.is_real_node() and node == parent.right:
            node = parent
            parent = parent.parent
        return parent
