from typing import Dict, Tuple, TypeVar, Generic, Optional

from src.hw4.treap.node import Node

K = TypeVar("K")
V = TypeVar("V")


def _merge(left_root: Optional[Node], right_root: Optional[Node]) -> Optional[Node]:
    if right_root is None:
        return left_root
    elif left_root is None:
        return right_root

    if left_root.priority > right_root.priority:
        left_root.right = _merge(left_root.right, right_root)
        return left_root
    else:
        right_root.left = _merge(left_root, right_root.left)
        return right_root


def _split(root: Node, key: K) -> Tuple[Optional[Node], Optional[Node]]:
    if root is None:
        return None, None

    if key > root.key:
        left_root, right_root = _split(root.right, key)
        root.right = left_root
        return root, right_root
    else:
        left_root, right_root = _split(root.left, key)
        root.left = right_root
        return left_root, root


def _find_in(node: Optional[Node], key: K) -> Optional[Node]:
    if node is None:
        return None

    if key == node.key:
        return node

    if key > node.key:
        return _find_in(node.right, key)
    else:
        return _find_in(node.left, key)


class Treap(Generic[K, V]):
    def __init__(self, *args):
        self.root = None
        if len(args) == 1:
            init_object = args[0]
            if isinstance(init_object, Dict):
                self._build(init_object)
            elif isinstance(init_object, Node):
                self.root = init_object

    def __getitem__(self, key: K) -> Optional[V]:
        found_node = _find_in(self.root, key)
        if found_node is not None:
            return found_node.priority

        return None

    def __setitem__(self, key: K, priority: V):
        inserting_node = Node(key, priority)
        if self.root is None:
            self.root = inserting_node
            return

        if key in self:
            self.remove(key)
        left_root, right_root = _split(self.root, key)
        treap_left = _merge(left_root, inserting_node)
        merged_treaps_root = _merge(treap_left, right_root)
        self.root = merged_treaps_root

    def __contains__(self, key: K):
        if self.root is None:
            return False

        return _find_in(self.root, key) is not None

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

        left_root, right_root = _split(self.root, key)

        def _remove_left(node: Optional[Node], node_parent: Optional[Node]):
            if node is None:
                return

            if node.key == key:
                node_parent.left = node.right
                return

            _remove_left(node.left, node)

        if right_root.key == key:
            right_root = right_root.right
        else:
            _remove_left(right_root, None)

        merged_treaps_root = _merge(left_root, right_root)
        self.root = merged_treaps_root

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
