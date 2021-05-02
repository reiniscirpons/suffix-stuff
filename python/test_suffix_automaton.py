""" Tests for SuffixAutomaton """
from typing import List, Dict
import random
import pytest
import suffix_automaton

AutomatonTransition = Dict[suffix_automaton.Letter, suffix_automaton.State]
AutomatonStructure = Dict[suffix_automaton.State, AutomatonTransition]
def verify_automaton_structure(automaton: suffix_automaton.SuffixAutomaton,
                               structure: AutomatonStructure,
                               root: suffix_automaton.State):
    """ Given an automaton check that it has the given structure. """
    if len(automaton.states) != len(structure):
        # Must have same number of states
        return False
    que = [(automaton.root_id, root)]
    translation = {}
    translation[root] = automaton.root_id
    i = 0
    while i < len(que):
        u, v = que[i]
        if automaton.states[u].transition.keys() != structure[v].keys():
            # All transitions must occur!
            return False
        for a in structure[v]:
            s = structure[v][a]
            t = automaton.states[u].transition[a].state_id
            if s in translation and translation[s] != t:
                # Every state must have a unique state representing it in the
                # structure
                return False
            if s not in translation:
                # Add new pair to check
                translation[s] = t
                que.append((t, s))
        i += 1
    if len(translation) != len(structure):
        return False
    return True

@pytest.mark.parametrize("word, structure, structure_root",
        [([0, 0],
          {0: {0: 1},
           1: {0: 2},
           2: {}},
          0),
         ([0, 1, 0],
          {0: {0: 1, 1: 2},
           1: {1: 2},
           2: {0: 3},
           3: {}},
          0),
         ([0, 1, 1],
          {0: {0: 1, 1: 4},
           1: {1: 2},
           2: {1: 3},
           3: {},
           4: {1: 3}},
          0),
         ([2, 1, 1, 0, 1, 0],
          {0: {2: 1, 1: 4, 0: 8},
           1: {1: 2},
           2: {1: 3},
           3: {0: 5},
           4: {1: 3, 0: 8},
           5: {1: 6},
           6: {0: 7},
           7: {},
           8: {1: 6}},
          0),
         ([0, 1, 2, 1, 2],
          {0: {0: 1, 1: 4, 2: 7},
           1: {1: 2},
           2: {2: 3},
           3: {1: 5},
           4: {2: 7},
           5: {2: 6},
           6: {},
           7: {1: 5}},
          0),
         ([0, 1, 1, 1],
          {0: {0: 1, 1: 5},
           1: {1: 2},
           2: {1: 3},
           3: {1: 4},
           4: {},
           5: {1: 6},
           6: {1: 4}
          },
          0),
         ([4, 0, 1, 0, 1, 4],
          {0: {4: 1, 0: 7, 1: 8},
           1: {0: 2},
           2: {1: 3},
           3: {0: 4},
           4: {1: 5},
           5: {4: 6},
           6: {},
           7: {1: 8},
           8: {0: 4, 4: 6}
          },
          0)
        ])
def test_add_word(word, structure, structure_root):
    """ Check that SuffixAutomaton.add_word operates correctly. """
    A = suffix_automaton.SuffixAutomaton([])
    A.add_word(word)
    assert verify_automaton_structure(A, structure, structure_root)

@pytest.mark.parametrize("words, structure, structure_root",
        [([[0, 0]],
          {0: {0: 1},
           1: {0: 2},
           2: {}},
          0),
         ([[0, 1, 0]],
          {0: {0: 1, 1: 2},
           1: {1: 2},
           2: {0: 3},
           3: {}},
          0),
         ([[0, 1, 1]],
          {0: {0: 1, 1: 4},
           1: {1: 2},
           2: {1: 3},
           3: {},
           4: {1: 3}},
          0),
         ([[0, 0], [0, 1, 0]],
          {0: {0: 1, 1: 3},
           1: {0: 2, 1: 3},
           2: {},
           3: {0: 2}},
          0),
         ([[0, 1, 0], [0, 0]],
          {0: {0: 1, 1: 3},
           1: {0: 2, 1: 3},
           2: {},
           3: {0: 2}},
          0),
         ([[0, 1, 1, 2, 1, 2], [0, 1, 2, 0, 1]],
          {0: {0: 1, 1: 4, 2: 3},
           1: {1: 2},
           2: {1: 5, 2: 8},
           3: {0: 9, 1: 7},
           4: {1: 5, 2: 3},
           5: {2: 6},
           6: {1: 7},
           7: {2: 10},
           8: {0: 9},
           9: {1: 10},
           10: {}},
          0),
         ([[2, 2, 0, 2, 0], [0, 1, 0, 1, 0]],
          {0: {0: 6, 1: 7, 2: 1},
           1: {0: 6, 2: 2},
           2: {0: 3},
           3: {2: 4},
           4: {0: 5},
           5: {},
           6: {1: 7},
           7: {0: 8},
           8: {1: 4}},
          0)
        ])
def test_add_multiple_words(words, structure, structure_root):
    """ Check that SuffixAutomaton.__init__() operates correctly. """
    A = suffix_automaton.SuffixAutomaton(words)
    for i in range(len(A.states)):
        print(i, ": {", end = "")
        for a in A.states[i].transition:
            print(a, ":", A.states[i].transition[a].state_id, end =", ")
        print("}")
    assert verify_automaton_structure(A, structure, structure_root)

def random_word(k: int, 
                A: List[suffix_automaton.Letter]) -> suffix_automaton.Word:
    """ Generate a random k letter word with letters in A """
    return random.choices(A, k=k)

def random_words(n: int, k: int, A: List[suffix_automaton.Letter]
                 ) -> List[suffix_automaton.Word]:
    """ Generate n random words with k letters in A """
    return [random_word(k, A) for _ in range(n)]


@pytest.mark.parametrize("generator, repetitions",
        [(lambda: random_words(1, 10, [0, 1, 2]), 10),
         (lambda: random_words(1, 20, [5, 6, 10, 11]), 10),
         (lambda: random_words(1, 100, list(range(26))), 10),
         (lambda: random_words(2, 5, [0, 1, 2]), 10)])
         #(lambda: random_words(5, 10, [0, 1, 2]), 10),
         #(lambda: random_words(10, 20, [5, 6, 10, 11]), 10),
         #(lambda: random_words(10, 100, list(range(26))), 10)])
def test_state_count(generator, repetitions):
    """ Check that the state.count parameter is set correctly """
    for _ in range(repetitions):
        words = generator()
        print(words)
        A = suffix_automaton.SuffixAutomaton(words)
        substring_counts = {}
        for word in words:
            for i in range(len(word)):
                for j in range(i, len(word)):
                    s = tuple(word[i:j+1])
                    if s not in substring_counts:
                        substring_counts[s] = 0
                    substring_counts[s] += 1
        for s in substring_counts:
            state_id = A.traverse(s)
            assert state_id != -1
            print(s)
            assert A.states[state_id].count == substring_counts[s]

