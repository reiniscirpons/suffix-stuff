""" Implements a suffix automaton based solution """

# References
# [1]: cp-algorithms.com/string/suffix-automaton.html
# [2]: en.wikipedia.org/wiki/Suffix_automaton

from __future__ import annotations
from typing import Dict, Tuple, List, Optional, Set


# Some type aliases
StateId = int
Letter = int
Word = Tuple[Letter, ...]

class State:
    """ A suffix automaton state.

    Attributes:
        state_id:    An integer representing position of the state in the
                     automatons state list.
        length:      The length of the longest substring ending at this state.
        count:       The number of occurences of the longest substring ending at
                     this state.
        is_terminal: A boolean telling us if the state is terminal
        suffix_link: The state corresponding to the longest suffix of the
                     substrings ending at this state, that is distinct from the
                     current state.
        transition:  A dictionary that holds the local transitions. If a letter
                     `x` of the alphabet is in transition, then `transition[x]`
                     is the state we arrive at by appending `x` to the current
                     substring.
    """
    def __init__(self,
                 state_id: StateId,
                 length: int,
                 suffix_link: Optional[State] = None,
                 transition: Optional[Dict[Letter, State]] = None):
        self.state_id = state_id
        self.length = length
        self.suffix_link = suffix_link
        # Count will get updated by the automaton, it is wrong at initialization
        self.count = 0
        # Incorrect at initialization, will get updated later.
        self.is_terminal = False
        # Use a dict since the automaton will be sparse, so we will have a lot
        # of empty transitions
        # TODO: Maybe a single global dict is better than many small dicts?
        self.transition: Dict[Letter, State]
        if transition is None:
            self.transition = {}
        else:
            self.transition = transition

    def __str__(self):
        return str((self.state_id, dict((letter, state.state_id) for\
                                    letter, state in self.transition.items())))

    def __repr__(self):
        repr_dict = {"state_id": self.state_id,
                     "transition": dict((letter, state.state_id) for\
                                    letter, state in self.transition.items())}
                     
        if self.suffix_link is not None:
            repr_dict["suffix_link"] = self.suffix_link.state_id
        else:
            repr_dict["suffix_link"] = -1

        repr



class SuffixAutomaton:
    """ A suffix automaton.

    Attributes:
        states: A collection of all the automaton states.
        root_id:   The id of the initial state (currently always 0).
    """

    def __init__(self, words: List[Word]):
        """ Initialize a suffix automaton.

        Args:
            words: The list of words that should be used to make the automaton.
        """
        self.states: List[State] = []
        # This is constant
        self.root_id: StateId = 0
        self.states.append(State(state_id=self.root_id, length=0))

        for word in words:
            self.add_word(word)

        # Make suffix states terminal, and update counts
        for word in words:
            state: Optional[State] = self.states[self.root_id]
            for letter in word:
                # Transition is guaranteed to exist by construction
                state = state.transition[letter]
                state.count += 1

            while state is not None:
                state.is_terminal = True
                state = state.suffix_link

        # Update number of occurrences
        self.recompute_count()

    def add_word(self, word: Word) -> None:
        """ Adds a single word to the automaton.

        Modifies the automaton so that it accepts all the suffixes of word in
        addition to any that it already accepts.

        Args:
            word: The word to insert.
        """
        last_state: Optional[State] = self.states[self.root_id]

        for letter in word:
            last_state = self.add_letter(letter, last_state)


    def add_letter(self, letter: Letter, last_state: Optional[State]) -> State:
        """ Add a single letter transition to a given state, return new state.

        Args:
            letter:     The letter transition to be added.
            last_state: Where we finished off after adding the last letter.

        Returns:
            The final state after inserting the letter.
        """
        if last_state is None:
            last_state = self.states[self.root_id]

        new_state: Optional[State] = None
        if letter not in last_state.transition:
            new_state = State(state_id=len(self.states),
                              length=last_state.length + 1)
            self.states.append(new_state)

            while last_state is not None and \
                  letter not in last_state.transition:
                last_state.transition[letter] = new_state
                last_state = last_state.suffix_link

            if last_state is None:
                new_state.suffix_link = self.states[self.root_id]
                return new_state

        paralell_state: State = last_state.transition[letter]
        if paralell_state.length == last_state.length + 1:
            if new_state is not None:
                new_state.suffix_link = paralell_state
                return new_state
            return paralell_state

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

        if new_state is not None:
            new_state.suffix_link = clone_state
            return new_state
        return clone_state

    # Utility
    def traverse(self, word: Word) -> Optional[State]:
        """ Traverse the word letter by letter through the automaton.

        Args:
            word: The word to be traversed.

        Returns:
            The final state we end up in, or -1 if the word does not define a
            valid path in the automaton (i.e. if we "fall off" the automaton
            during traversal).
        """
        state = self.states[self.root_id]
        for letter in word:
            if letter not in state.transition:
                return None
            state = state.transition[letter]
        return state

    def accepts(self, word: Word) -> bool:
        """ Return true is automaton accepts word and false otherwise. """
        state = self.traverse(word)
        return state is not None and state.is_terminal

    def language(self) -> Set[Word]:
        """ Compute the language accepted by the automaton. """
        right_languages: List[Set[Word]] = \
            [set() for _ in range(len(self.states))]


        topo = self.topological_sort()
        while len(topo)>0:
            state = topo.pop()
            if state.is_terminal:
                # Add empty word
                right_languages[state.state_id].add(tuple())

            for letter in state.transition:
                child = state.transition[letter]
                for word in right_languages[child.state_id]:
                    right_languages[state.state_id].add((letter,)+word)

        return right_languages[self.root_id]

    def topological_sort(self) -> List[State]:
        """ Returns the list of states of the automaton in topological order.

        Assumes the automaton is connected.

        Returns:
            A list of states so that all the parents of a state occur before the
            state.
        """

        indegree = [0 for _ in range(len(self.states))]
        for state in self.states:
            for child in state.transition.values():
                indegree[child.state_id] += 1

        # Something is deeply wrong if this doesn't hold
        assert indegree[self.root_id] == 0
        topo = [self.states[self.root_id]]
        c = 0
        while c < len(topo):
            state = topo[c]
            for child in state.transition.values():
                indegree[child.state_id] -= 1
                if indegree[child.state_id] == 0:
                    topo.append(child)
            c += 1

        return topo


    def recompute_length(self) -> None:
        """ Update all the states length parameter.

        The length of a state is the length of the longest word ending in that
        state. This function recomputes the length for every state.
        """

        self.states[self.root_id].length = 0
        sorted_states = self.topological_sort()
        for state in sorted_states:
            for child in state.transition.values():
                child.length = max(child.length, state.length + 1)

    def recompute_count(self) -> None:
        """ Update all the states count parameter.

        The count of a state is the number of times the substring represented by
        the word occurs in the text.
        """
        states = self.topological_sort()
        while len(states) > 0:
            state = states.pop()
            if state.suffix_link is not None:
                state.suffix_link.count += state.count

    def __repr__(self):
        repr_dict = {"initial": self.root_id,
                     "state_transitions": {},
                     "terminal": set(),
                     "suffix_links": {},
                     "lengths": {},
                     "counts": {}}
        for state in self.states:
            repr_dict["state_transitions"][state.state_id] = {}
            for letter in state.transition:
                repr_dict["state_transitions"][state.state_id][letter] = \
                    state.transition[letter].state_id

            if state.is_terminal:
                repr_dict["terminal"].add(state.state_id)

            if state.suffix_link is not None:
                repr_dict["suffix_links"][state.state_id] = \
                    state.suffix_link.state_id
            else:
                repr_dict["suffix_links"][state.state_id] = -1

            repr_dict["lengths"][state.state_id] = state.length

            repr_dict["counts"][state.state_id] = state.count

        return repr(repr_dict)
