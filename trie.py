
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

    def get_all(self):
        """Get all of the words in the Trie"""
        item_list = []
        self._get_all(self.root, "", item_list)
        return item_list

    def _get_all(self, root, pre, items):
        """
        recursively visit all the levels of the Trie
        :param root:
        :param pre:
        :param items:
        :return:
        """
        if not root:
            return
        for key, node in root.items():
            if key.endswith("_end"):
                items.append(pre + key[0])
            self._get_all(node, pre+key[0], items)

    def __len__(self):
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
        """
        :param word: the word to delete
        :return: if the word is in the Trie, returns the word itself, else returns None
        """
        current = self.root
        length = len(word)
        n = 0
        for letter in word:
            n += 1
            if length == n:
                if current.get(letter + "_end", None) is not None:
                    current[letter] = current.pop(letter + "_end", {})
                    self.items_number -= 1
                    return word
                else:
                    return None
            else:
                current = current.get(letter)
                if current is None:
                    return None

    def __repr__(self):
        pass

    def __str__(self):
        pass


if __name__ == '__main__':
    tr = Trie()
    for word in ("first", "second", "security", "name", "access", "butterfly", "serious", "seashells", "sea"):
        tr.put(word)
    for word in ("first", "second", "security", "name", "lksdfw", "car", "seashore"):
        print(word in tr)
    print(tr.get_all())
    print(tr.delete("second"))
    print(tr.get_all())
