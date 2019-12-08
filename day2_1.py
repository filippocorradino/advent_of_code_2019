#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 2 - Challenge 1
https://adventofcode.com/2019/day/2

Solution: 2890696

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode


def main():
    program = Intcode()
    program.load_from_file('inputs/day_2_input.txt')
    program.dsky(12, 2)
    program.execute()
    print("\nFinal value at position 0: {0}\n".format(program.memory[0]))
    return program.memory[0]


if __name__ == "__main__":
    main()
