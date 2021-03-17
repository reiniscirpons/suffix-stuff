# Suffix stuff

The aim of this repo is to explore various datastructures and algorithms for
computing statistics of subwords for a collection of words. We will primarily
explore suffix-based structures, such as suffix arrays, trees, automata and so
on, since these seem to be well suited for the particular task.

## The problem
We are mainly interested in solving the following problems:

> **Problem 1**:
> Given a collection of words find the number of occurrences of each subword
> and sort them in descending order according to the product of the length of
> the subword and number of occurences (or similar metric).

We call Problem 1 the subword occurence metric problem.

To define the second problem we introduce the following definition:
Given a collection of words `w_1, ..., w_n` we define a _piece_ to be any
word `v` that has at least two occurences as a subword of the `w_i`'s
(this can be either in the same or in different words). 

> **Problem 2**:
> Given a collection of words `w_1, ..., w_n`, for every word `w_i` find a
> greedy factorization of it into pieces, that is, find a sequence of subwords
> `v_i1, ... v_ik` such that `w_i = v_i1 * ... * v_ik`, each of the `v_ik` is a
> piece, and furthermore, `v_i1` is the largest such prefix of `w_i`, `v_i2` is
> the largest such prefix of the remainder of `w_i` after removing `v_i1` etc.

We call Problem 2 the greedy piece factorization problem.

## Workflow
The current workflow is structured as follows:
1. Implement a prototype of a problem solution in python. Also make tests here
   etc.
2. Convert the prototype to a C++ implementation (and port over the tests).
3. Do some benchmarking on the C++ implementation and optimize as necessary

## Note
This repository is part of the 2020/2021 Mathematical Software Vertically
Integrated Project at the University of St Andrews.

