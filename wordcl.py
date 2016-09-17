

class Trie:
    """
    Trie data structure for storing a set of words
    Python dictionary is used for internal implementation
    The end of the word is marked with "_end" at the end of a key.
    """
    def __init__(self):
        self.root = dict()

    def __contains__(self, word):
        current = self.root
        length = len(word)
        n = 0
        for letter in word:
            n += 1
            if length == n:
                return current.get(letter+"_end")
            else:
                current = current.get(letter)
                if current is None:
                    return None

    def __getitem__(self, word):
        if self.__contains__(word):
            return word
        else:
            None

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

    def __repr__(self):
        pass

    def __str__(self):
        pass
