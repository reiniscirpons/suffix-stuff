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
    que = [(automaton.root, root)]
    translation = {}
    translation[root] = automaton.root
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
        [("aa",
          {0: {"a": 1},
           1: {"a": 2},
           2: {}},
          0),
         ("aba",
          {0: {"a": 1, "b": 2},
           1: {"b": 2},
           2: {"a": 3},
           3: {}},
          0),
         ("abb",
          {0: {"a": 1, "b": 4},
           1: {"b": 2},
           2: {"b": 3},
           3: {},
           4: {"b": 3}},
          0),
         ("abbcbc",
          {0: {"a": 1, "b": 4, "c": 8},
           1: {"b": 2},
           2: {"b": 3},
           3: {"c": 5},
           4: {"b": 3, "c": 8},
           5: {"b": 6},
           6: {"c": 7},
           7: {},
           8: {"b": 6}},
          0),
         ("abcbc",
          {0: {"a": 1, "b": 4, "c": 7},
           1: {"b": 2},
           2: {"c": 3},
           3: {"b": 5},
           4: {"c": 7},
           5: {"c": 6},
           6: {},
           7: {"b": 5}},
          0),
         ("abbb",
          {0: {"a": 1, "b": 5},
           1: {"b": 2},
           2: {"b": 3},
           3: {"b": 4},
           4: {},
           5: {"b": 6},
           6: {"b": 4}
          },
          0),
         ("dababd",
          {0: {"d": 1, "a": 7, "b": 8},
           1: {"a": 2},
           2: {"b": 3},
           3: {"a": 4},
           4: {"b": 5},
           5: {"d": 6},
           6: {},
           7: {"b": 8},
           8: {"a": 4, "d": 6}
          },
          0)
        ])
def test_add_word(word, structure, structure_root):
    """ Check that SuffixAutomaton.add_word operates correctly. """
    A = suffix_automaton.SuffixAutomaton([])
    A.add_word(word)
    assert verify_automaton_structure(A, structure, structure_root)

@pytest.mark.parametrize("words, structure, structure_root",
        [(["aa"],
          {0: {"a": 1},
           1: {"a": 2},
           2: {}},
          0),
         (["aba"],
          {0: {"a": 1, "b": 2},
           1: {"b": 2},
           2: {"a": 3},
           3: {}},
          0),
         (["abb"],
          {0: {"a": 1, "b": 4},
           1: {"b": 2},
           2: {"b": 3},
           3: {},
           4: {"b": 3}},
          0),
         (["aa", "aba"],
          {0: {"a": 1, "b": 3},
           1: {"a": 2, "b": 3},
           2: {},
           3: {"a": 2}},
          0),
         (["aba", "aa"],
          {0: {"a": 1, "b": 3},
           1: {"a": 2, "b": 3},
           2: {},
           3: {"a": 2}},
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
