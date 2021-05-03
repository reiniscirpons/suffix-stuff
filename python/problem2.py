""" Implement solution to greedy piece factorization problem """
from typing import List
import suffix_automaton

def greedy_piece_factorization(words: List[suffix_automaton.Word]) \
        -> List[List[int]]:
    """ Solve greedy piece factorization

    Args:
        A list of words to factorize.

    Returns:
        A list consisting of lists of the end positions of each piece. That is
        to say, if the entry corresponding to word w_i is [a_1, ..., a_n], then
        the pieces of w_i are w_i[0:a_1], w_i[a_1:a_2], ..., w_i[a_{n-1}, a_n].
        If the list is empty, then w_i does not possess a greedy piece
        factorization.
    """

    A = suffix_automaton.SuffixAutomaton(words)

    pieces = []
    for word in words:
        factorization: List[int] = []
        state = A.states[A.root_id]
        for i, letter in enumerate(word):
            if state.transition[letter].count <= 1:
                if i == 0 or i == factorization[-1]+1:
                    # Cant factor
                    factorization = []
                    break
                factorization.append(i)
                state = A.states[A.root_id]
            else:
                state = state.transition[letter]
        pieces.append(factorization)

    return pieces
