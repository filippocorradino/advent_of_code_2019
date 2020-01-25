#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 9 - Challenge 2
https://adventofcode.com/2019/day/9

Solution: 76791

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode


def main():
    program = Intcode()
    program.load_from_file('inputs/day_9_input.txt')
    program.input(2)
    program.execute()
    while program.output_buffer:
        coordinates = program.output()
    print("Distress signal coordinates are: {0}\n".format(coordinates))
    return coordinates


if __name__ == "__main__":
    main()
