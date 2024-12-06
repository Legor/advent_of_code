class TreeNode:
    """A node in a binary tree."""

    def __init__(self, value):
        """
        Initialize a tree node.

        Args:
            value: The value of the node.
        """
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    """A simple binary tree."""

    def __init__(self):
        """
        Initialize an empty binary tree.
        """
        self.root = None
        self.leafs = {}

    def __getitem__(self, item):
        if item in self.leafs:
            return self.leafs[item]

    def add_leaf(self, value, children=(None, None)):
        """
        Add a node to the tree with optional left and right children.

        Args:
            value: The value of the node to add.
            children (tuple): A tuple (left_child_value, right_child_value).
                              Use None for no child.

        Returns:
            The newly created node.
        """
        if value not in self.leafs:
            self.leafs[value] = TreeNode(value)

        node = self.leafs[value]

        if not self.root:
            self.root = node

        left_value, right_value = children

        if left_value is not None:
            if left_value not in self.leafs:
                self.leafs[left_value] = (
                    TreeNode(left_value) if left_value != value else node
                )
            node.left = self.leafs[left_value]

        if right_value is not None:
            if right_value not in self.leafs:
                self.leafs[right_value] = (
                    TreeNode(right_value) if right_value != value else node
                )
            node.right = self.leafs[right_value]

        return node

    def left(self, parent_value):
        """
        Get the left child of a given node.

        Args:
            parent_value: The value of the parent node.

        Returns:
            The child node, or None if the child does not exist.
        """
        parent_node = self.leafs.get(parent_value)
        if parent_node:
            return parent_node.left
        return None

    def right(self, parent_value):
        """
        Get the right child of a given node.

        Args:
            parent_value: The value of the parent node.

        Returns:
            The child node, or None if the child does not exist.
        """
        parent_node = self.leafs.get(parent_value)
        if parent_node:
            return parent_node.right
        return None

    def print(self, node, level=0, prefix="Root: ", visited=None):
        """
        Print the tree in a hierarchical format.

        Args:
            node: The current node to print.
            level: The current level in the tree.
            prefix: The prefix to print before the node value.
        """
        if node is None:
            return

        if visited is None:
            visited = set()

            # Check for circular dependency
        if node in visited:
            print(" " * (level * 4) + prefix + str(node.value) + " (circular)")
            return
        else:
            visited.add(node)

        print(" " * (level * 4) + prefix + str(node.value))
        self.print(node.left, level + 1, "L--- ", visited)
        self.print(node.right, level + 1, "R--- ", visited)
