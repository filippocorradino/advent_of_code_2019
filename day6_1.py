#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 6 - Challenge 1
https://adventofcode.com/2019/day/6

Solution: 261306

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Orbiter


def import_orbitmap():
    bodies = {}
    bodies.update({'COM': Orbiter(bodies)})
    with open('inputs/day_6_input.txt') as file:
        for line in file:
            line = line.rstrip()
            main, orbiter = line.split(')')
            bodies.update({orbiter: Orbiter(bodies, main)})
    return bodies


def main():
    bodies = import_orbitmap()
    totalCount = sum(x.get_orbits() for x in bodies.values())
    print("\nTotal orbit count is: {0}\n".format(totalCount))
    return totalCount


if __name__ == "__main__":
    main()
