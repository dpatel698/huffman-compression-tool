import sys
from collections import Counter
import heapq
from HuffmanCoder import HuffmanTree


def get_char_frequencies(text):
    frequencies = Counter(text)
    return frequencies


def compress_text(text, code_table):
    output = ""
    for char in text:
        output += code_table[char]
    return output


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-e":
            with open(sys.argv[2], "r", encoding="utf-8") as file:
                file_text = file.read()
                char_counts = get_char_frequencies(file_text)
                min_heap = []
                for char, val in char_counts.items():
                    heapq.heappush(min_heap, HuffmanTree(char, val))
                # Generate Tree and Prefix Code Table
                tree = HuffmanTree.buildTree(min_heap)
                code_table = tree.generate_code_table()
                # Compress the given file
                with open("compressed_" + sys.argv[2], "w", encoding="utf-8") as out_file:
                    tree_encoding = HuffmanTree.serialize(tree.get_root())
                    out_file.write(tree_encoding + "\n")
                    out_file.write(compress_text(file_text, code_table))
                    out_file.close()
                file.close()

    except FileNotFoundError:
        print(f"{sys.argv[1]} not found")
