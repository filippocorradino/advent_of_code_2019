#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 1 - Challenge 1
https://adventofcode.com/2019/day/1

Solution: 3348909

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


def required_fuel(module_mass):
    fuel = int(module_mass/3) - 2
    return fuel


def main():
    fuel = 0
    with open('inputs/day_01_input.txt') as file:
        for line in file:
            fuel = fuel + required_fuel(int(line))
    print("\nFinal fuel count: {0}\n".format(fuel))
    return fuel


if __name__ == "__main__":
    main()
