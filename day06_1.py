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
    bodies['COM'] = Orbiter(bodies)
    with open('inputs/day_06_input.txt') as file:
        for line in file:
            line = line.rstrip()
            main_body, orbiter = line.split(')')
            bodies[orbiter] = Orbiter(bodies, main_body)
    return bodies


def main():
    bodies = import_orbitmap()
    total_count = sum(x.get_orbits() for x in bodies.values())
    print("\nTotal orbit count is: {0}\n".format(total_count))
    return total_count


if __name__ == "__main__":
    main()
