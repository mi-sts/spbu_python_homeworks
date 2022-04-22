import random
from copy import deepcopy
from typing import Generic, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    def __init__(self, key: K, data: V, left: Optional["Node"] = None, right: Optional["Node"] = None):
        self.key = key
        self.data = data
        self.priority = random.random()
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

    def __deepcopy__(self, memo):
        node_copy = Node(self.key, self.data)
        node_copy.priority = self.priority
        if self.left is not None:
            node_copy.left = deepcopy(self.left)
        if self.right is not None:
            node_copy.right = deepcopy(self.right)
        return node_copy

    def __eq__(self, other):
        return (
            isinstance(other, Node)
            and other.key == self.key
            and other.data == self.data
            and other.priority == self.priority
            and self.left == other.left
            and self.right == other.right
        )

    def get_pair(self) -> Tuple[K, V]:
        return self.key, self.data

    def _node_item_to_string(self):
        return f"Node({self.key}, {self.data})"
