""" Implements a suffix automaton based solution """

# References
# [1]: cp-algorithms.com/string/suffix-automaton.html
# [2]: en.wikipedia.org/wiki/Suffix_automaton

from __future__ import annotations
from typing import Dict, List, Optional


# Some type aliases
StateId = int
Letter = int
Word = List[Letter]

class State:
    """ A suffix automaton state.

    Attributes:
        state_id:    An integer representing position of the state in the
                     automatons state list.
        length:      The length of the longest substring ending at this state.
        suffix_link: The state corresponding to the longest suffix of the
                     substrings ending at this state, that is distinct from the
                     current state.
        transition:  A dictionary that holds the local transitions. If a letter
                     `x` of the alphabet is in transition, then `transition[x]`
                     is the state we arrive at by appending `x` to the current
                     substring.
    """
    def __init__(self, state_id, length, suffix_link=None, transition=None):
        # Should be constant
        self.state_id: StateId = state_id
        self.length: int = length
        self.suffix_link: Optional[State] = suffix_link
        # Use a dict since the automaton will be sparse, so we will have a lot
        # of empty transitions
        # TODO: Maybe a single global dict is better than many small dicts?
        self.transition: Dict[Letter, State]
        if transition is None:
            self.transition = {}
        else:
            self.transition = transition

class SuffixAutomaton:
    """ A suffix automaton.

    Attributes:
        states: A collection of all the automaton states.
        root:   The initial state (currently always 0).
    """

    def __init__(self, words: List[Word]):
        """ Initialize a suffix automaton.

        Args:
            words: The list of words that should be used to make the automaton.
        """
        self.states: List[State] = []
        # This is constant
        self.root: StateId = 0
        self.states.append(State(state_id=self.root, length=0))

        if len(words) == 0:
            pass
        elif len(words) == 1:
            # Simple case, no need to do anything complicated
            self.add_word(words[0])
        else:
            # Make a letter that definitely does not occur in the word
            l = max(map(max, words)) + 1

            big_word = []
            for i, word in enumerate(words):
                for letter in word:
                    big_word.append(letter)
                big_word.append(l + i)

            self.add_word(big_word)
            
            # Now we go through and remove all non-letter links
            for state in self.states:
                for i in range(len(words)):
                    if l+i in state.transition:
                        del state.transition[l+i]

            #TODO: Now apply a minimization algorithm


    def add_word(self, word: Word, last_state: Optional[State] = None) -> State:
        """ Adds a single word to the automaton and return final state.

        Args:
            word: The word to insert.

        Returns:
            The final state after inserting all letters.
        """
        if last_state is None:
            last_state = self.states[self.root]

        for letter in word:
            last_state = self.add_letter(letter, last_state)
        return last_state

    def add_letter(self, letter: Letter, last_state: Optional[State]) -> State:
        """ Add a single letter transition to a given state, return new state.

        Args:
            letter:     The letter transition to be added.
            last_state: Where we finished off after adding the last letter.

        Returns:
            The final state after inserting the letter.
        """
        if last_state is None:
            last_state = self.states[self.root]

        new_state: State = State(state_id=len(self.states),
                                 length=last_state.length + 1)
        self.states.append(new_state)

        while last_state is not None and \
              letter not in last_state.transition:
            last_state.transition[letter] = new_state
            last_state = last_state.suffix_link

        if last_state is None:
            new_state.suffix_link = self.states[self.root]
            return new_state

        paralell_state: State = last_state.transition[letter]
        if paralell_state.length == last_state.length + 1:
            new_state.suffix_link = paralell_state
            return new_state

        clone_state: State = State(state_id=len(self.states),
                                   length=last_state.length + 1,
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

    def traverse(self, word: Word) -> StateId:
        """ Traverse the word letter by letter through the automaton.

        Args:
            word: The word to be traversed.

        Returns:
            The final state we end up in, or -1 if the word does not define a
            valid path in the automaton (i.e. if we "fall off" the automaton
            during traversal).
        """
        state = self.states[self.root]
        for letter in word:
            if letter not in state.transition:
                return -1
            state = state.transition[letter]
        return state.state_id
