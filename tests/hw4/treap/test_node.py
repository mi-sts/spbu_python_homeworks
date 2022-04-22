import pytest
from copy import deepcopy

from src.hw4.treap.node import Node

#
#                            (7, 10)
#                            /     \
#                       (5, 8)     (8, 9)
#                       /               \
#                 (-2, 7)               (12, 5)
#                        \              /     \
#                        (-1, 6)  (10, 3)     (16, 2)
node_tree = Node(
    7, 10, Node(5, 8, Node(-2, 7, None, Node(-1, 6))), Node(8, 9, None, Node(12, 5, Node(10, 3), Node(16, 2)))
)


def get_node_pairs(node: Node):
    return [node.get_pair() for node in node]


def test_repr():
    parent_node = Node(2, 8, Node(4, 6))
    assert repr(parent_node) == "Node(2, 8), left-Node(4, 6), right-None\nNode(4, 6), left-None, right-None\n"


def test_get_pair():
    node = Node(1, 2)
    assert node.get_pair() == (1, 2)


def test_iter():
    assert get_node_pairs(node_tree) == [(7, 10), (5, 8), (-2, 7), (-1, 6), (8, 9), (12, 5), (10, 3), (16, 2)]


def test_deepcopy_accordance():
    node = Node(1, 2, Node(3, 4), Node(5, 6, Node(7, 8)))
    node_deepcopy = deepcopy(node)
    assert get_node_pairs(node) == get_node_pairs(node_deepcopy)


def test_deepcopy_change_independent():
    node = Node(1, 2, Node(3, 4), Node(5, 6, Node(7, 8)))
    node_deepcopy = deepcopy(node)
    node_deepcopy.right = Node(10, 10)
    assert node.right.get_pair() != (10, 10)
