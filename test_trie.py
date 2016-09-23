from trie import Trie

if __name__ == '__main__':
    tr = Trie()
    with open("words.txt") as file:
        for line in file:
            tr.put(line.strip())
    print(tr.size())