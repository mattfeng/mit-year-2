#!/usr/bin/env python

from text_tokenize import tokenize_sentences

class Trie:
    def __init__(self):
        self.value = None
        self.children = dict()
        self.type = None

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if self.type is None:
            self.type = type(key)
        
        if type(key) is not self.type:
            raise TypeError("Can't set using wrongly typed key: `{}`".format(key))

        if len(key) == 0:
            self.value = value
            return

        child = key[0]
        if child not in self.children:
            self.children[child] = Trie()
        self.children[child][key[1:]] = value


    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """

        if type(key) is not self.type:
            raise TypeError("Can't get using wrongly typed key: `{}`".format(key))

        if len(key) == 0:
            if self.value is None:
                raise KeyError("Key is not inside trie")
            else:
                return self.value
        
        return self.children[key[0]][key[1:]]


    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        self[key] = None


    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        return self[key] is not None

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        if self.value is not None:
            yield (self.type(), self.value)
            
        for key, child in self.children.items():
            for suffix, val in child:
                yield (key + suffix, val)
        

def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    raise NotImplementedError


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    raise NotImplementedError


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    raise NotImplementedError


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    raise NotImplementedError


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    raise NotImplementedError


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    s = Trie()
    s["hi"] = 1
    s["hip"] = 3
    s["hipster"] = 5
    for i in s:
        print(i)
