#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 13 - Challenge 1
https://adventofcode.com/2019/day/13

Solution: 247

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode


def main():
    screen = {}
    program = Intcode()
    program.load_from_file('inputs/day_13_input.txt')
    program.execute()
    while program.output_buffer:
        x = program.output()
        y = program.output()
        v = program.output()
        screen.update({(x, y): v})
    n_blocks = sum(x == 2 for x in screen.values())
    print("\nThere are a total of {0} blocks\n".format(n_blocks))
    return n_blocks


if __name__ == "__main__":
    main()
