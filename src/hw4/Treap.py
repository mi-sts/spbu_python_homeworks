from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Tuple


class ChildSide(Enum):
    LEFT = 0
    RIGHT = 1
    NONE = 2


@dataclass
class Node:
    key: object = 0
    priority: object = 0
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def __repr__(self):
        representation = ""
        for node in self:
            representation += f"{node._node_item_to_string()}, "
            if node.left is not None:
                representation += f"left-{node.left._node_item_to_string()}, "
            else:
                representation += "left-None, "
            if node.right is not None:
                representation += f"right-{node.right._node_item_to_string()}\n"
            else:
                representation += "right-None\n"

        return representation

    def __iter__(self):
        yield self
        if self.left is not None:
            yield from iter(self.left)
        if self.right is not None:
            yield from iter(self.right)

    def __contains__(self, key):
        return self.find(key) is not None

    def set_child(self, child: Optional["Node"], side: ChildSide):
        if child is None:
            return
        if side == ChildSide.LEFT:
            self.left = child
        elif side == ChildSide.RIGHT:
            self.right = child

    def get_child(self, side: ChildSide) -> Optional["Node"]:
        if side == ChildSide.LEFT:
            return self.left
        elif side == ChildSide.RIGHT:
            return self.right

    def get_child_by_key(self, key: object) -> Tuple[Optional["Node"], ChildSide]:
        if key >= self.key:
            return self.right, ChildSide.RIGHT

        return self.left, ChildSide.LEFT

    def insert(self, node: "Node"):
        if node.key >= self.key:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)
        else:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)

    def split(self, key: object) -> Tuple[Optional["Node"], Optional["Node"]]:
        if key >= self.key:
            if self.right is None:
                return self, None
            left_part, right_part = self.right.split(key)
            self.right = left_part

            return self, right_part
        else:
            if self.left is None:
                return None, self
            left_part, right_part = self.left.split(key)
            self.left = right_part

            return left_part, self

    def find(self, key: object) -> Optional["Node"]:
        if key == self.key:
            return self

        if key > self.key:
            if self.right is None:
                return None

            return self.right.find(key)
        else:
            if self.left is None:
                return None

            return self.left.find(key)

    def find_parent(self, key: object) -> Tuple[Optional["Node"], ChildSide]:
        return self._find_parent(key, None, ChildSide.NONE)

    def merge_with(self, node: Optional["Node"]) -> "Node":
        if node is None:
            return self
        if self.priority > node.priority:
            if self.right is None:
                self.right = node
                return self
            else:
                return self.right.merge_with(node)
        else:
            if node.left is None:
                node.left = self
                return node
            else:
                return self.merge_with(node.left)

    def _find_parent(
        self, key: object, current_parent: Optional["Node"], current_side: ChildSide
    ) -> Tuple[Optional["Node"], ChildSide]:
        if key == self.key:
            return current_parent, current_side

        if key > self.key:
            if self.right is None:
                return None, ChildSide.RIGHT

            return self.right._find_parent(key, self, ChildSide.RIGHT)
        else:
            if self.left is None:
                return None, ChildSide.LEFT

            return self.left._find_parent(key, self, ChildSide.LEFT)

    def _node_item_to_string(self):
        return f"Node({self.key}, {self.priority})"


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

        set_node_parent, set_node_side = self.root.find_parent(key)
        if set_node_parent.get_child(set_node_side) is None:
            set_node_parent.set_child(Node(key, priority), set_node_side)
        else:
            set_node_parent.get_child(set_node_side).priority = priority

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

        self.root.merge_with(treap.root)

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
