import sys
from collections import Counter
import heapq
from HuffmanCoder import HuffmanTree
import base64


def get_char_frequencies(text):
    frequencies = Counter(text)
    return frequencies


def compress_prefixes(binary_prefixes):
    concatenated = ''.join(binary_prefixes)

    # Pad the concatenated string to ensure its length is a multiple of 8
    padding = 8 - (len(concatenated) % 8) if len(concatenated) % 8 != 0 else 0
    padded = concatenated + '0' * padding

    # Convert the padded binary string to bytes
    compressed = int(padded, 2).to_bytes(len(padded) // 8, byteorder='big')

    return compressed, padding


def decompress_prefixes(compressed, padding):
    # Convert bytes to a binary string
    binary = ''.join(format(byte, '08b') for byte in compressed)

    # Remove padding
    binary = binary[:-padding] if padding else binary

    return binary


def compress_text(text, code_table):
    prefixes = []
    for char in text:
        prefixes.append(code_table[char])
    return compress_prefixes(prefixes)


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
                with open("compressed_" + sys.argv[2], "wb") as out_file:
                    tree_encoding = HuffmanTree.serialize(tree.get_root()) + "\n"
                    out_file.write(tree_encoding.encode("utf-8"))
                    compressed, padding = compress_text(file_text, code_table)
                    out_file.write((str(padding) + "\n").encode("utf-8"))
                    compressed_b64 = base64.b64encode(compressed)
                    out_file.write(compressed_b64)
        if sys.argv[1] == "-d":
            with open(sys.argv[2], "r", encoding="utf-8") as file:
                file_text = file.read()
                tree_encoding, padding, compressed_text = file_text.split("\n")
                compressed_text = base64.b64decode(compressed_text)
                compressed_text = decompress_prefixes(compressed_text, int(padding))

                # Generate the Huffman Tree from the compressed header
                huff_node, huff_tree = HuffmanTree.deserialize(tree_encoding), HuffmanTree()
                huff_tree.set_root(huff_node)

                # Decompress the binary text using the tree to decode and write to a file
                with open("decompressed_" + sys.argv[2], "wb") as out_file:
                    out_file.write(huff_tree.decode(compressed_text).replace("\\n", "\n").encode("utf-8"))
    except FileNotFoundError:
        print(f"{sys.argv[2]} not found")
