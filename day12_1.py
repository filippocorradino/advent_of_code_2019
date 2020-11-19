#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 12 - Challenge 1
https://adventofcode.com/2019/day/12

Solution: 8625

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import LunarSystem


def main():
    system = LunarSystem.import_moons('inputs/day_12_input.txt')
    system.propagate(steps=1000)
    total_energy = system.total_energy()
    print("\nThe total energy of the system is {0}\n".format(total_energy))
    return total_energy


if __name__ == "__main__":
    main()
