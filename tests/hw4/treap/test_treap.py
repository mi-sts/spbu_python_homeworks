import pytest
from copy import deepcopy
from src.hw4.treap.node import Node
from src.hw4.treap.treap import Treap, _split, _merge

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
tree_elements = {7: 10, 12: 5, 8: 9, 16: 2, 10: 3, 5: 8, -1: 6, -2: 7}


def get_treap_pairs(treap: Treap):
    return [node.get_pair() for node in treap]


def test_init_with_dict():
    treap = Treap(tree_elements)
    assert get_treap_pairs(treap) == [node.get_pair() for node in node_tree]


def test_init_with_root_node():
    treap = Treap(deepcopy(node_tree))
    assert get_treap_pairs(treap) == [node.get_pair() for node in node_tree]


def test_get_item_successful():
    treap = Treap(tree_elements)
    assert treap[-2] == 7


def test_get_item_unsuccessful():
    treap = Treap(tree_elements)
    assert treap[-10] is None


def test_set_item_new():
    treap = Treap(deepcopy(node_tree))
    treap[11] = 7
    assert get_treap_pairs(treap) == [(7, 10), (5, 8), (-2, 7), (-1, 6), (8, 9), (11, 7), (10, 3), (12, 5), (16, 2)]


def test_set_item_overwriting():
    treap = Treap(deepcopy(node_tree))
    treap[-2] = 9
    assert get_treap_pairs(treap) == [(7, 10), (-2, 9), (5, 8), (-1, 6), (8, 9), (12, 5), (10, 3), (16, 2)]


def test_set_item_change_root():
    treap = Treap(deepcopy(node_tree))
    treap[15] = 20
    assert get_treap_pairs(treap) == [(15, 20), (7, 10), (5, 8), (-2, 7), (-1, 6), (8, 9), (12, 5), (10, 3), (16, 2)]


def test_contain():
    treap = Treap(deepcopy(node_tree))
    assert 16 in treap


def test_not_contain():
    treap = Treap(deepcopy(node_tree))
    assert 9 not in treap


def test_repr():
    treap = Treap(deepcopy(node_tree))
    assert (
        repr(treap) == "Treap():\n"
        "Node(7, 10), left-Node(5, 8), right-Node(8, 9)\n"
        "Node(5, 8), left-Node(-2, 7), right-None\n"
        "Node(-2, 7), left-None, right-Node(-1, 6)\n"
        "Node(-1, 6), left-None, right-None\n"
        "Node(8, 9), left-None, right-Node(12, 5)\n"
        "Node(12, 5), left-Node(10, 3), right-Node(16, 2)\n"
        "Node(10, 3), left-None, right-None\n"
        "Node(16, 2), left-None, right-None\n"
    )


def test_iter():
    treap = Treap(deepcopy(node_tree))
    assert get_treap_pairs(treap) == [(7, 10), (5, 8), (-2, 7), (-1, 6), (8, 9), (12, 5), (10, 3), (16, 2)]


def test_split():
    treap = Treap(deepcopy(node_tree))
    left_root, right_root = _split(treap.root, 9)
    assert get_treap_pairs(Treap(left_root)) == [(7, 10), (5, 8), (-2, 7), (-1, 6), (8, 9)]
    assert get_treap_pairs(Treap(right_root)) == [(12, 5), (10, 3), (16, 2)]


def test_merge_with():
    first_treap = Treap(deepcopy(node_tree))
    second_treap = Treap({20: 9, 22: 15, 26: 2})
    treap = Treap(_merge(first_treap.root, second_treap.root))
    assert get_treap_pairs(treap) == [
        (22, 15),
        (7, 10),
        (5, 8),
        (-2, 7),
        (-1, 6),
        (20, 9),
        (8, 9),
        (12, 5),
        (10, 3),
        (16, 2),
        (26, 2),
    ]


def test_remove():
    treap = Treap(deepcopy(node_tree))
    treap.remove(12)
    assert get_treap_pairs(treap) == [(7, 10), (5, 8), (-2, 7), (-1, 6), (8, 9), (10, 3), (16, 2)]
