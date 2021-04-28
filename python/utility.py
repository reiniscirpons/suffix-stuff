""" Just some utility functions and type definitions """
from typing import List, Tuple

def radix_sort():
    # TODO

def unify_equal_tuples(T: List[Tuple[int, ...]]) -> List[int]:
    """ Given a list of tuples, find a unique representative to each.

    The result is a list representative of integers such that
    T[i] = T[representative[i]] and 
    T[i] = T[j] if and only if representative[i] = representative[j].
    Uses a radix sort based approach.
    """
    R = []


