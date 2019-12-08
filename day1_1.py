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


def required_fuel(moduleMass):
    fuel = int(moduleMass/3) - 2
    return fuel


def main():
    fuel = 0
    with open('inputs/day_1_input.txt') as file:
        for line in file:
            fuel = fuel + required_fuel(int(line))
    print("\nFinal fuel count: {0}\n".format(fuel))
    return


if __name__ == "__main__":
    main()