""" Implements a suffix automaton based solution """

# References
# [1]: cp-algorithms.com/string/suffix-automaton.html
# [2]: en.wikipedia.org/wiki/Suffix_automaton

from __future__ import annotations
from typing import NamedTuple, Dict, List

Letter = int
Word = List[Letter]
class State(NamedTuple):
    """ A suffix automaton state.

    Attributes:
        length: The length of the longest substring ending at this state.
        suffix_link: The state corresponding to the longest suffix of the
        substrings ending at this state.
        transition: A dictionary that holds the local transitions. If a letter x
        of the alphabet is in transition, then transition[x] is the state we
        arrive at by appending x to the current substring.
    """
    length: int
    suffix_link: State = None
    # Use a dict since the automaton will be sparse, so we will have a lot of
    # empty transitions
    transition: Dict[Letter, State] = {}

class SuffixAutomaton:
    """ A suffix automaton.

    Attributes:
        states: A collection of all the automaton states.
        root: the initial state (always 0)
    """

    def __init__(self, words: List[Word]):
        """ Initialize a suffix automaton.

        Args:
            words: The set of words that should be used to make the automaton.
        """
        self.states = [None]
        # This is constant
        self.root = 0
        self.states[self.root] = State(length=0)
        for word in words:
            self.add_word(word)

    def add_word(self, word: Word) -> State:
        """ Adds a single word to the automaton and return final state.

        Args:
            word: The word to insert.

        Returns:
            The final state after inserting all letters.
        """
        last_state = self.states[self.root]
        for letter in word:
            last_state = self.add_letter(letter, last_state)
        return last_state

    def add_letter(self, letter: Letter, last_state: State) -> State:
        """ Add a single letter transition to a given state, return new state.

        Args:
            letter: The letter transition to be added.
            last_state: Where we finished off after adding the last letter.

        Returns:
            The final state after inserting the letter.
        """
        new_state = State(length=last_state.length + 1)
        self.states.append(new_state)

        while last_state is not None and \
              letter not in last_state.transition:
            last_state.transition[letter] = new_state
            last_state = last_state.suffix_link

        if last_state is None:
            new_state.suffix_link = self.root
            return new_state

        paralell_state = last_state.transition[letter]
        if paralell_state.length == last_state.length + 1:
            new_state.suffix_link = paralell_state
            return new_state

        clone_state = State(length=last_state.length + 1,
                            suffix_link=paralell_state.suffix_link,
                            transition=paralell_state.transition.copy())
        self.states.append(clone_state)
        while last_state is not None and \
              last_state.transition[letter] is paralell_state:
            last_state.transition[letter] = clone_state
            last_state = last_state.suffix_link
        paralell_state.suffix_link = clone_state
        new_state.suffix_link = clone_state

        return new_state
