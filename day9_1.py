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
    program.load_from_file('inputs/day_9_input.txt')
    program.input(1)
    program.execute()
    while program.outputBuffer:
        keyCode = program.output()
    print("BOOST key code is: {0}\n".format(keyCode))
    return keyCode


if __name__ == "__main__":
    main()
