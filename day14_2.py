#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 14 - Challenge 2
https://adventofcode.com/2019/day/14

Solution: 2267486

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from day14_1 import main as cost_function


def main(n_source=1000000000000):
    n_target = 1
    # The function n_source = f(n_target) is surely concave
    # This is because for higher n_target, we can optimize some reactions
    # We'll apply the secant method to reach an approximate solution
    while cost_function(n_target=n_target) < n_source:
        est_target_to_source = cost_function(n_target=n_target) // n_target
        n_target = n_source // est_target_to_source
    # Refine the solution
    while cost_function(n_target=n_target) > n_source:
        n_target = n_target - 1
    print("\nNumber of FUEL achievable with {0} ORE: {1}\n"
          .format(n_source, n_target))
    return n_target


if __name__ == "__main__":
    main()
