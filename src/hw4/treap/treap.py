from src.hw4.treap.node import Node
from typing import Dict, Tuple


class Treap:
    def __init__(self, init_object: Dict | Node):
        self.root = None
        if isinstance(init_object, Dict):
            self._build(init_object)
        elif isinstance(init_object, Node):
            self.root = init_object

    def __getitem__(self, key) -> object:
        if self.root is None:
            return None

        return self.root.find(key)

    def __setitem__(self, key, priority):
        if self.root is None:
            self.root = Node(key, priority)
            return

        inserting_node = Node(key, priority)
        self.root.insert(inserting_node)
        if self.root.priority < priority:
            self.root = inserting_node

    def __contains__(self, item):
        if self.root is None:
            return False

        return item in self.root

    def __repr__(self):
        if self.root is None:
            root_representation = "None"
        else:
            root_representation = repr(self.root)

        return f"Treap():\n{root_representation}"

    def __iter__(self):
        if self.root is not None:
            yield from iter(self.root)

    def __del__(self):
        self.root = None

    def split(self, key: object) -> Tuple["Treap", "Treap"]:
        left_root, right_root = self.root.split(key)
        return Treap(left_root), Treap(right_root)

    def merge_with(self, treap: "Treap"):
        if self.root is None:
            self.root = treap.root
            return

        self.root = self.root.merge_with(treap.root)

    def remove(self, key: object):
        if self.root is None:
            return

        removing_node_parent, removing_node_side = self.root.find_parent(key)
        if removing_node_parent is None:
            return
        removing_node = removing_node_parent.get_child(removing_node_side)
        if removing_node.left is not None:
            merged_children = removing_node.left.merge_with(removing_node.right)
        else:
            merged_children = removing_node.right
        removing_node_parent.set_child(merged_children, removing_node_side)

    def _build(self, elements: Dict):
        sorted_elements = sorted(map(lambda item: Node(item[0], item[1]), elements.items()), key=lambda item: item.key)
        parents = [None] * len(elements)
        self.root = sorted_elements[0]

        def _building_insert(parent_index: int, inserting_index: int, parent_right_index: int = None):
            parent = sorted_elements[parent_index]
            adding_node = sorted_elements[inserting_index]
            if adding_node.priority < parent.priority:
                if parent_right_index is None:
                    parent.right = adding_node
                else:
                    parent.right, adding_node.left = adding_node, parent.right
                    parents[parent_right_index] = inserting_index
                parents[inserting_index] = parent_index

            elif parent == self.root:
                self.root, adding_node.left = adding_node, parent
                parents[inserting_index], parents[parent_index] = None, inserting_index
            else:
                _building_insert(parents[parent_index], inserting_index, parent_index)

        for i in range(1, len(sorted_elements)):
            _building_insert(i - 1, i)
