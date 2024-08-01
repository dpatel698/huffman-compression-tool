# Defines and implements nodes and tree for Huffman Coding
from __future__ import annotations

import collections
import heapq


class HuffmanNode:

    def __init__(self, char=None, weight=None, left=None, right=None):
        self.char = char
        self.weight = weight
        self.left = left
        self.right = right

    def get_value(self) -> str:
        return self.char

    def get_weight(self) -> int:
        return self.weight

    def get_left(self) -> HuffmanNode:
        return self.left

    def get_right(self) -> HuffmanNode:
        return self.right

    def is_leaf(self):
        return not self.left and not self.right


class HuffmanTree:

    def __init__(self, char=None, weight=None, tree1: HuffmanTree = None, tree2: HuffmanTree = None):
        if tree1 and tree2:
            self.root = HuffmanNode(char, weight, tree1.get_root(), tree2.get_root())
        else:
            self.root = HuffmanNode(char, weight)

    def get_root(self) -> HuffmanNode:
        return self.root

    def set_root(self, root: HuffmanNode):
        self.root = root

    def weight(self) -> int:
        return self.root.get_weight()

    def __lt__(self, other: HuffmanTree):
        return self.weight() < other.weight()

    @staticmethod
    def serialize(root):
        """
        Converts the Huffman Tree into a string form that can be saved to a file
        :return: string encoding of the Huffman Tree
        """
        out = []
        q = collections.deque([root])
        while q:
            node = q.pop()
            if node:
                if node.is_leaf():
                    value = node.get_value()
                    if value == "\n":
                        value = "\\n"
                    out.append(str(node.get_weight()) + "|" + value)
                else:
                    out.append(str(node.get_weight()))
                q.appendleft(node.get_left())
                q.appendleft(node.get_right())
            else:
                out.append("N")
        return ",".join(out)

    @staticmethod
    def deserialize_node_encoding(i, flat_data):
        weight, char = None, None
        if "|" in flat_data[i]:
            contents = flat_data[i].split("|")
            weight = int(contents[0])
            if len(contents) == 3:
                char = "|"
            else:
                char = "," if contents[1] == "" else contents[1]
        else:
            weight = int(flat_data[i])
        return HuffmanNode(weight=weight, char=char)

    @staticmethod
    def deserialize(data):
        """
        Converts a string encoding into a Huffman Tree
        :return: Huffman Tree
        """
        if not data:
            return
        flat_data = data.split(',')
        root = HuffmanNode(weight=int(flat_data[0]))
        queue = collections.deque([root])
        i = 1
        # when you pop a node, its children will be at i and i+1
        while queue:
            node = queue.pop()
            if flat_data[i] == '':
                i += 1
            if i < len(flat_data) and flat_data[i] != "N":
                node.left = HuffmanTree.deserialize_node_encoding(i, flat_data)
                queue.appendleft(node.left)
            i += 1
            if flat_data[i] == '':
                i += 1
            if i < len(flat_data) and flat_data[i] != "N":
                node.right = HuffmanTree.deserialize_node_encoding(i, flat_data)
                queue.appendleft(node.right)
            i += 1
        return root

    @staticmethod
    def buildTree(huff_heap: list[HuffmanTree]) -> HuffmanTree:
        while len(huff_heap) > 1:
            tree1 = heapq.heappop(huff_heap)
            tree2 = heapq.heappop(huff_heap)

            tree3 = HuffmanTree(None, tree1.weight() + tree2.weight(), tree1, tree2)
            heapq.heappush(huff_heap, tree3)

        return heapq.heappop(huff_heap)

    def generate_code_table(self):
        return self.__get_code_table(self.root)

    def __get_code_table(self, node: HuffmanNode, move_left=False, code=""):
        if node.is_leaf():
            return {node.get_value(): code}
        table = dict()
        table.update(self.__get_code_table(node.get_left(), True, code + "0"))
        table.update(self.__get_code_table(node.get_right(), False, code + "1"))
        return table

    def decode(self, code):
        """
        Decodes a binary code using the Huffman Tree.
        Moving left in the tree is "0" and right is "1".
        :param code: a binary code
        :return: a string decoding
        """
        decoding = ""
        i = 0
        curr = self.get_root()
        while i <= len(code):
            if curr.is_leaf():
                decoding += curr.get_value()
                curr = self.get_root()
                if i == len(code):
                    break
            elif code[i] == "0":
                curr = curr.get_left()
                i += 1
            else:
                curr = curr.get_right()
                i += 1
        return decoding









