""" Implement suffix tree based solution """
from typing import List
from suffix_automaton import Letter, Word, SuffixAutomaton

# States are for automata, nodes are for trees.
NodeId = int

def SuffixTree:
    """ Suffix tree """
    def __init__(words: List[word]):
        """Given a list of words, return their suffix automaton.
        """
        # The parent node of current node
        self.parent: List[NodeId] = []
        # For a given
        self.child: Dict[Letter, NodeId] = []

        # Make a letter that definitely does not occur in the word
        l = max(map(max, words)) + 1

        # Need to concatenate and reverse words so we produce a suffix instead
        # of a prefix tree. This therefore is actually a prefix automaton, but
        # that is a minor detail.
        big_reverse_word = []
        for i, word in enumerate(words):
            big_reverse_word.append(l + i)
            for letter in reversed(word):
                big_reverse_word.append(letter)

        A = SuffixAutomaton([])
        A.add_word(big_reverse_word)


    

