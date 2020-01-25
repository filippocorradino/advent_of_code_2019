#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 2 - Challenge 2
https://adventofcode.com/2019/day/2

Solution: 8226

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode


def main():
    output = 19690720
    program = Intcode()
    program.load_from_file('inputs/day_2_input.txt')
    for noun, verb in \
            [(noun, verb) for noun in range(0, 100) for verb in range(0, 100)]:
        program.rewind()
        program.dsky(noun, verb)
        program.execute()
        if program.memory[0] == output:
            break
    program_code = 100*noun+verb
    print("\nThe program outputting {0} is: {1:04d} "
          "(noun {2:02d} - verb {3:02d})\n"
          .format(program.memory[0], program_code, noun, verb))
    return program_code


if __name__ == "__main__":
    main()
