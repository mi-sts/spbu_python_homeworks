from copy import deepcopy
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple


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

    def __deepcopy__(self, memo):
        node_copy = Node(self.key, self.priority)
        if self.left is not None:
            node_copy.left = deepcopy(self.left)
        if self.right is not None:
            node_copy.right = deepcopy(self.right)
        return node_copy

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

    def _insert(self, node: "Node", parent_node: Optional["Node"], node_side: ChildSide):
        if self.priority < node.priority:
            left_node, right_node = self.split(node.key)
            node.left, node.right = left_node, right_node
            if parent_node is not None:
                parent_node.set_child(node, node_side)
        else:
            child_node, child_side = self.get_child_by_key(node.key)
            if child_node is not None:
                child_node._insert(node, self, child_side)
            else:
                self.set_child(node, node_side)

    def insert(self, node: "Node"):
        self._insert(node, None, ChildSide.NONE)

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

            self.right = self.right.merge_with(node)
            return self
        else:
            if node.left is None:
                node.left = self
                return node

            node.left = self.merge_with(node.left)
            return node

    def get_pair(self) -> Tuple[object, object]:
        return self.key, self.priority

    def _find_parent(
        self, key: object, current_parent: Optional["Node"], current_side: ChildSide
    ) -> Tuple[Optional["Node"], ChildSide]:
        if key == self.key:
            return current_parent, current_side

        if key > self.key:
            if self.right is None:
                return self, ChildSide.RIGHT

            return self.right._find_parent(key, self, ChildSide.RIGHT)
        else:
            if self.left is None:
                return self, ChildSide.LEFT

            return self.left._find_parent(key, self, ChildSide.LEFT)

    def _node_item_to_string(self):
        return f"Node({self.key}, {self.priority})"
