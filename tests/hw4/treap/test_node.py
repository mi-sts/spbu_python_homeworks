from typing import Optional

import pytest
from copy import deepcopy
from src.hw4.treap.node import ChildSide
from src.hw4.treap.treap import Node

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


def test_contains():
    assert 12 in node_tree


def test_not_contains():
    assert 2 not in node_tree


def test_set_child():
    node = Node(1, 2)
    child = Node(3, 4)
    node.set_child(child, ChildSide.RIGHT)
    assert node.right == child


def test_get_child():
    node = Node(1, 2, Node(3, 4), Node(5, 6))
    assert node.get_child(ChildSide.LEFT) == Node(3, 4)


def test_get_child_by_key_greater():
    node = Node(1, 2, Node(3, 4), Node(5, 6))
    assert node.get_child_by_key(10) == (Node(5, 6), ChildSide.RIGHT)


def test_get_child_by_key_less():
    node = Node(1, 2, Node(3, 4), Node(5, 6))
    assert node.get_child_by_key(0) == (Node(3, 4), ChildSide.LEFT)


def test_deepcopy_accordance():
    node = Node(1, 2, Node(3, 4), Node(5, 6, Node(7, 8)))
    node_deepcopy = deepcopy(node)
    assert get_node_pairs(node) == get_node_pairs(node_deepcopy)


def test_deepcopy_change_independent():
    node = Node(1, 2, Node(3, 4), Node(5, 6, Node(7, 8)))
    node_deepcopy = deepcopy(node)
    node_deepcopy.set_child(Node(10, 10), ChildSide.RIGHT)
    assert node.get_child(ChildSide.RIGHT).get_pair() != (10, 10)


def test_merge_with():
    node_tree_copy = deepcopy(node_tree)
    merged_nodes = Node(-10, 16, Node(-14, 12), Node(-7, 15, Node(-8, 13), Node(-5, 11, None, Node(-3, 5)))).merge_with(
        node_tree_copy
    )
    assert get_node_pairs(merged_nodes) == [
        (-10, 16),
        (-14, 12),
        (-7, 15),
        (-8, 13),
        (-5, 11),
        (7, 10),
        (5, 8),
        (-2, 7),
        (-3, 5),
        (-1, 6),
        (8, 9),
        (12, 5),
        (10, 3),
        (16, 2),
    ]


def test_split():
    node_tree_copy = deepcopy(node_tree)
    left_node, right_node = node_tree_copy.split(0)
    assert left_node == Node(-2, 7, None, Node(-1, 6))
    assert right_node == Node(7, 10, Node(5, 8), Node(8, 9, None, Node(12, 5, Node(10, 3), Node(16, 2))))


def test_insert_1():
    node_tree_copy = deepcopy(node_tree)
    node_tree_copy.insert(Node(10, 5))
    assert get_node_pairs(node_tree_copy) == [
        (7, 10),
        (5, 8),
        (-2, 7),
        (-1, 6),
        (8, 9),
        (12, 5),
        (10, 5),
        (10, 3),
        (16, 2),
    ]


def test_insert_2():
    node_tree_copy = deepcopy(node_tree)
    node_tree_copy.insert(Node(17, 1))
    assert get_node_pairs(node_tree_copy) == [
        (7, 10),
        (5, 8),
        (-2, 7),
        (-1, 6),
        (8, 9),
        (12, 5),
        (10, 3),
        (16, 2),
        (17, 1),
    ]


def test_insert_change_root():
    node_tree_copy = deepcopy(node_tree)
    inserting_node = Node(3, 12)
    node_tree_copy.insert(inserting_node)
    assert get_node_pairs(inserting_node) == [
        (3, 12),
        (-2, 7),
        (-1, 6),
        (7, 10),
        (5, 8),
        (8, 9),
        (12, 5),
        (10, 3),
        (16, 2),
    ]


def test_find_successful():
    assert node_tree.find(12).get_pair() == (12, 5)


def test_find_unsuccessful():
    assert node_tree.find(-10) is None


def test_find_parent():
    parent_node, child_side = node_tree.find_parent(12)
    assert (parent_node.get_pair(), child_side == (8, 9), ChildSide.RIGHT)
