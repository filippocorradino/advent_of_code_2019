#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 9 - Challenge 1
https://adventofcode.com/2019/day/9

Solution: 3989758265

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode


def main():
    program = Intcode()
    program.load_from_file('inputs/day_09_input.txt')
    program.input(1)
    program.execute()
    while program.output_buffer:
        key_code = program.output()
    print("\nBOOST key code is: {0}\n".format(key_code))
    return key_code


if __name__ == "__main__":
    main()
