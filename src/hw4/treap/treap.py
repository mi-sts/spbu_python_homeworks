from typing import Dict, Tuple, TypeVar, Generic

from src.hw4.treap.node import Node

K = TypeVar("K")
V = TypeVar("V")


class Treap(Generic[K, V]):
    def __init__(self, *args):
        self.root = None
        if len(args) == 1:
            init_object = args[0]
            if isinstance(init_object, Dict):
                self._build(init_object)
            elif isinstance(init_object, Node):
                self.root = init_object

    def __getitem__(self, key: K) -> V:
        if self.root is None:
            return None

        item = self.root.find(key)
        if item is not None:
            return item.priority

        return None

    def __setitem__(self, key: K, priority: V):
        if self.root is None:
            self.root = Node(key, priority)
            return

        inserting_node = Node(key, priority)
        self.root.insert(inserting_node)
        if self.root.priority < priority:
            self.root = inserting_node

    def __contains__(self, key: K):
        if self.root is None:
            return False

        return key in self.root

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

    def remove(self, key: K):
        if self.root is None:
            return

        if self.root.key == key:
            self.root = None
            return

        self.root.remove(key)

    def _split(self, key: K) -> Tuple["Treap", "Treap"]:
        left_root, right_root = self.root.split(key)
        return Treap(left_root), Treap(right_root)

    def _merge_with(self, treap: "Treap"):
        if self.root is None:
            self.root = treap.root
            return

        self.root = self.root.merge_with(treap.root)

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
