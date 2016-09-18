
class Trie:
    """
    Trie data structure for storing a set of words
    Python dictionary is used for internal implementation
    The end of the word is marked with "_end" at the end of a key.
    """
    def __init__(self):
        self.root = dict()
        self.items_number = 0

    def __contains__(self, word):
        current = self.root
        length = len(word)
        n = 0
        for letter in word:
            n += 1
            if length == n:
                return current.get(letter + "_end") is not None
            else:
                current = current.get(letter)
                if current is None:
                    return None

    def __getitem__(self, word):
        if self.__contains__(word):
            return word
        else:
            return None

    def collect(self):
        pass

    def get_all(self):
        """Get all of the words in the trie"""
        item_list = []
        self._get_all(self.root, "", item_list)
        return item_list

    def _get_all(self, root, pre, items):
        if not root:
            return
        for key, node in root.items():
            if key.endswith("_end"):
                items.append(pre + key[0])
            self._get_all(node, pre+key[0], items)

    def size(self):
        return self.items_number

    def put(self, word):
        current = self.root
        length = len(word)
        n = 0
        for letter in word:
            n += 1
            if length == n:
                insert = letter + "_end"
            else:
                insert = letter
            current = current.setdefault(insert, {})
        self.items_number += 1

    def delete(self, word):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

if __name__ == '__main__':
    tr = Trie()
    tr.put("first")
    tr.put("second")
    tr.put("security")
    print("first" in tr)
    print("none" in tr)
    print(tr.get_all())
