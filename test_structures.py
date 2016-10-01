import sys
from trie import Trie
from bloom_filter import BloomFilter
from tools import get_size

if __name__ == '__main__':
    bf_dups = 0
    tr = Trie()
    bf = BloomFilter(capacity=700000, error_rate=0.001)
    with open("words.txt") as file:
        for line in file:
            tr.put(line.strip())
            if bf.put(line.strip()):
                print("Duplicate in bloom filter: {0}".format(line.strip()))
                bf_dups += 1

    print("Trie. number of objects put: {0}".format(len(tr)))
    print("Bloom filter. number of objects put: {0}".format(len(bf)))
    print()
    print("Trie. Size of the object: {0}".format(sys.getsizeof(tr)))
    print("Bloom filter. Size of the object: {0}".format(sys.getsizeof(bf)))
    print()
    print("Trie. Size of the object(full): {0}".format(get_size(tr)))
    print("Bloom filter. Size of the object(full): {0}".format(get_size(bf)))
    print()
    print("Bloom filter errors: {0}".format(bf_dups))
    print("----------------------------------------------------------")
