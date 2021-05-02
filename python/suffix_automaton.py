""" Implements a suffix automaton based solution """

# References
# [1]: cp-algorithms.com/string/suffix-automaton.html
# [2]: en.wikipedia.org/wiki/Suffix_automaton

from __future__ import annotations
from typing import Dict, Tuple, List, Optional


# Some type aliases
StateId = int
Letter = int
Word = List[Letter]
Signature = Tuple[Tuple[Letter, StateId], ...]

class State:
    """ A suffix automaton state.

    Attributes:
        state_id:    An integer representing position of the state in the
                     automatons state list.
        length:      The length of the longest substring ending at this state.
        count:       The number of occurences of the longest substring ending at
                     this state.
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
                 count: int,
                 suffix_link: Optional[State] = None,
                 transition: Optional[Dict[Letter, State]] = None):
        self.state_id= state_id
        self.length= length
        self.suffix_link = suffix_link
        # Count will get updated by the automaton, it is wrong at initialization
        self.count = count
        # Use a dict since the automaton will be sparse, so we will have a lot
        # of empty transitions
        # TODO: Maybe a single global dict is better than many small dicts?
        self.transition: Dict[Letter, State]
        if transition is None:
            self.transition = {}
        else:
            self.transition = transition

    def signature(self) -> Signature:
        """ Return the states signature.

        A signature is an encoding of a states transition as a tuple.
        If a state q has a transition to a states p_1, p_2, ..., p_n labeled by
        letters a_1, a_2, ..., a_n, then its signature is
        ((a_1, p_1), ..., (a_n, p_n))
        Where we assume a_1 < a_2 < ... < a_n
        Additionally, we differentiate a terminal state by adding an
        extra symbol to the state, but since all our states are terminal this is
        not of particular benefit to us currently.
        """
        signature = []
        for letter in sorted(self.transition):
            signature.append((letter, self.transition[letter].state_id))
        return tuple(signature)


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
        self.states.append(State(state_id=self.root_id, length=0, count=0))

        if len(words) == 0:
            pass
        elif len(words) == 1:
            # Simple case, no need to do anything complicated
            self.add_word(words[0])
            # Update number of occurrences
            self.recompute_count()
        else:
            # Make a letter that definitely does not occur in the word
            l = max(map(max, words)) + 1

            big_word = []
            for i, word in enumerate(words):
                for letter in word:
                    big_word.append(letter)
                big_word.append(l + i)

            self.add_word(big_word)

            # Update number of occurrences
            self.recompute_count()
            self.states[self.root_id].count -= len(words)

            # Now we go through and remove all non-letter links
            for state in self.states:
                for i in range(len(words)):
                    if l+i in state.transition:
                        del state.transition[l+i]

            # Remove all unreachable states
            self.connected_subautomaton()
            # Now apply a minimization algorithm
            self.minimize()




    def add_word(self, word: Word) -> State:
        """ Adds a single word to the automaton and return final state.

        Args:
            word: The word to insert.

        Returns:
            The final state after inserting all letters.
        """
        last_state = self.states[self.root_id]

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
            last_state = self.states[self.root_id]

        new_state: State = State(state_id=len(self.states),
                                 length=last_state.length + 1,
                                 count=1)
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
            new_state.suffix_link = paralell_state
            return new_state

        clone_state: State = State(state_id=len(self.states),
                                   length=last_state.length + 1,
                                   count=0,
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


    # Minimization

    def connected_subautomaton(self) -> None:
        """ Modify self in place to remove all disconnected states.

        A state of an automaton is disconnected if no path from the initial
        state can reach it or there is no path to a final state. In our case,
        every state is final, so we simply test the former.

        """
        connected_states = [self.states[self.root_id]]
        seen = [False for _ in range(len(self.states))]
        seen[self.root_id] = True
        c = 0
        while c < len(connected_states):
            state = connected_states[c]
            for child in state.transition.values():
                if not seen[child.state_id]:
                    seen[child.state_id] = True
                    connected_states.append(child)
            c += 1

        self.states = connected_states
        self.root_id = 0
        for i, state in enumerate(self.states):
            state.state_id = i

    def minimize(self) -> None:
        """ Modify self in place to yield a minimal automaton.

        Uses an algorithm known as Revuz minimization. We will divide the states
        into "layers" based on the length of the longest path leading into it.
        Then we minimize layer by layer, at each layer finding out hte
        equivalent states using a radix sort.
        """

        representative: List[StateId]
        representative = list(range(len(self.states)))

        max_length = max(state.length for state in self.states)
        layers: List[List[State]] = [[] for _ in range(max_length+1)]
        for state in self.states:
            layers[state.length].append(state)

        # In the original algorithm we would use a radix sort and whatnot, but
        # here we relegate to using a hash map since its quicker to implement
        # and likely has the same or better practical time complexity
        sig_to_rep: Dict[Signature, StateId] = {}
        for layer in reversed(layers):
            for state in layer:
                # Generate a "modified" signature, i.e.\ one where we replace
                # every state id by its representative in the current partially
                # minimized transducer
                temp_sig = []
                for letter in sorted(state.transition):
                    temp_sig.append((letter, \
                            representative[state.transition[letter].state_id]))
                mod_sig = tuple(temp_sig)
                # We are guaranteed that modified signatures are the same if and
                # only if two states are equivalent
                if mod_sig not in sig_to_rep:
                    sig_to_rep[mod_sig] = state.state_id
                else:
                    representative[state.state_id] = sig_to_rep[mod_sig]

        # Aggregate counts
        for state in self.states:
            if representative[state.state_id] != state.state_id:
                new_state = self.states[representative[state.state_id]]
                assert new_state.count == state.count

        # Now replace all states by representatives
        self.root_id = representative[self.root_id]
        new_states = [self.states[self.root_id]]
        seen = [False for _ in range(len(self.states))]
        seen[self.root_id] = True
        c = 0
        while c < len(new_states):
            state = new_states[c]
            if state.suffix_link is not None:
                new_suffix_link = self.states[representative[ \
                        state.suffix_link.state_id]]
                if new_suffix_link.state_id != state.state_id:
                    state.suffix_link = new_suffix_link
                else:
                    state.suffix_link = None
            for letter, child in state.transition.items():
                new_child = self.states[representative[child.state_id]]
                state.transition[letter] = new_child
                if not seen[new_child.state_id]:
                    seen[new_child.state_id] = True
                    new_states.append(new_child)
            c += 1

        self.states = new_states
        for i, state in enumerate(self.states):
            state.state_id = i

    # Utility

    def traverse(self, word: Word) -> StateId:
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
                return -1
            state = state.transition[letter]
        return state.state_id

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

        The length of a state is the length of the longest word ending in that
        state. This function recomputes the length for every state.
        """
        states = self.topological_sort()
        while len(states) > 0:
            state = states.pop()
            if state.suffix_link is not None:
                state.suffix_link.count += state.count
