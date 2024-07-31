import sys
from collections import Counter
import heapq
from HuffmanCoder import HuffmanTree


def get_char_frequencies(text):
    frequencies = Counter(text)
    return frequencies


if __name__ == "__main__":
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            file_text = file.read()
            char_counts = get_char_frequencies(file_text)
            min_heap = []
            for char, val in char_counts.items():
                heapq.heappush(min_heap, HuffmanTree(char, val))
            tree = HuffmanTree.buildTree(min_heap)
            code_table = tree.generate_code_table()
            print(code_table)
    except FileNotFoundError:
        print(f"{sys.argv[1]} not found")
