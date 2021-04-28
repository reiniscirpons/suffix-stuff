""" Tests for SuffixAutomaton """
from typing import Dict
import pytest
import suffix_automaton

def verify_automaton_structure(automaton: suffix_automaton.SuffixAutomaton,
                               structure: Dict[suffix_automaton.State,
                                               Dict[suffix_automaton.Letter,
                                                    suffix_automaton.State]],
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
