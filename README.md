# Suffix stuff

The aim of this repo is to explore various datastructures and algorithms for
computing statistics of subwords for a collection of words. We will primarily
explore suffix-based structures, such as suffix arrays, trees automata and so
on, since these seem to be well suited for the particular task.

## The problem
We are mainly interested in solving the following problem:

> Given a collection of words find then number of occurrences of each subword
> and sort them in descending order according to the product of the length of
> the subword and number of occurences (or similar metric)

A related problem is to return the collection of all subwords that occur more
than once.

## Workflow
The current workflow is structured as follows:
1. Implement a prototype of a problem solution in python. Also make tests here
   etc.
2. Convert the prototype to a C++ implementation (and port over the tests).
3. Do some benchmarking on the C++ implementation and optimize as necessary

## Note
This repository is part of the 2020/2021 Mathematical Software Vertically
Integrated Project at the University of St Andrews.

