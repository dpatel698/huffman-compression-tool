# Defines and implements nodes and tree for Huffman Coding
from __future__ import annotations
import heapq


class HuffmanNode:

    def __init__(self, char=None, weight=None, left=None, right=None):
        self.char = char
        self.weight = weight
        self.left = left
        self.right = right

    def value(self) -> str:
        return self.char

    def weight(self) -> int:
        return self.weight

    def left(self) -> HuffmanNode:
        return self.left

    def right(self) -> HuffmanNode:
        return self.right()

    def is_leaf(self):
        return not self.left and not self.right


class HuffmanTree:

    def __init__(self, tree1: HuffmanTree = None, tree2: HuffmanTree = None, char=None, weight=None):
        if tree1 or tree2:
            self.root = HuffmanNode(char, weight, tree1.get_root(), tree2.get_root())
        else:
            self.root = HuffmanNode(char, weight)

    def get_root(self):
        return self.root

    def weight(self) -> int:
        return self.root.weight()

    def __lt__(self, other: HuffmanTree):
        return self.weight() < other.weight()

    @staticmethod
    def buildTree(huff_heap: list[HuffmanTree]) -> HuffmanTree:
        while len(huff_heap) > 1:
            tree1 = heapq.heappop(huff_heap)
            tree2 = heapq.heappop(huff_heap)

            tree3 = HuffmanTree(tree1, tree2, None, tree1.weight() + tree2.weight())
            heapq.heappush(huff_heap, tree3)

        return heapq.heappop(huff_heap)

    def generate_code_table(self):
        return self.get_code_table(self.root)

    def get_code_table(self, node:HuffmanNode, move_left=False, code=""):
        if self.root.is_leaf():
            return {self.root.value(): code}
        table = dict()
        table.update(self.get_code_table(node.left(), True, code + "0"))
        table.update(self.get_code_table(node.right(), False, code + "1"))
        return table







