from copy import deepcopy
from typing import Generic, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    def __init__(self, key: K, priority: V, left: Optional["Node"] = None, right: Optional["Node"] = None):
        self.key = key
        self.priority = priority
        self.left = left
        self.right = right

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

    def __eq__(self, other):
        return (
            isinstance(other, Node)
            and other.key == self.key
            and other.priority == self.priority
            and self.left == other.left
            and self.right == other.right
        )

    def _insert(self, node: "Node", parent_node: Optional["Node"]):
        if self.priority < node.priority:
            left_node, right_node = self.split(node.key)
            node.left, node.right = left_node, right_node
            if parent_node is not None:
                parent_node._set_child_by_key(node, node.key)
        else:
            child_node = self._get_child_by_key(node.key)
            if child_node is not None:
                child_node._insert(node, self)
            else:
                self._set_child_by_key(node, node.key)

    def insert(self, node: "Node"):
        self._insert(node, None)

    def split(self, key: K) -> Tuple[Optional["Node"], Optional["Node"]]:
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

    def find(self, key: K) -> Optional["Node"]:
        if key == self.key:
            return self

        considered_child = self._get_child_by_key(key)
        if considered_child is None:
            return None

        return considered_child.find(key)

    def _find_parent(self, key: K, current_parent: Optional["Node"]) -> Optional["Node"]:
        if key == self.key:
            return current_parent

        considered_child = self._get_child_by_key(key)
        if considered_child is None:
            return self
        return considered_child._find_parent(key, self)

    def remove(self, key: K):
        removing_node_parent = self._find_parent(key, None)
        if removing_node_parent is None:
            return

        removing_node = removing_node_parent._get_child_by_key(key)

        if removing_node.left is not None:
            merged_children = removing_node.left.merge_with(removing_node.right)
        else:
            merged_children = removing_node.right

        removing_node_parent._set_child_by_key(merged_children, key)

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

    def get_pair(self) -> Tuple[K, V]:
        return self.key, self.priority

    def _set_child_by_key(self, child: Optional["Node"], key: K):
        if child is None:
            return
        if key >= self.key:
            self.right = child
        else:
            self.left = child

    def _get_child_by_key(self, key: K) -> Optional["Node"]:
        if key >= self.key:
            return self.right

        return self.left

    def _node_item_to_string(self):
        return f"Node({self.key}, {self.priority})"
