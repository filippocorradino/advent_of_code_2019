#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 5 - Challenge 2
https://adventofcode.com/2019/day/5

Solution: 5000972

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode


def main():
    program = Intcode()
    program.load_from_file('inputs/day_05_input.txt')
    program.input(5)
    program.execute()
    diagnostic_code = program.output()
    print("\nDiagnostic code is: {0}\n".format(diagnostic_code))
    return diagnostic_code


if __name__ == "__main__":
    main()
