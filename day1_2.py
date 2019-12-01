#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 1 - Challenge 2
https://adventofcode.com/2019/day/1

Solution: 5020494

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from day1_1 import required_fuel


def main():
    fuel = 0
    with open('inputs/day_1_input.txt') as file:
        for line in file:
            moduleFuel = 0
            newFuel = int(line)  # Initialize to module dry mass
            while True:
                # Iteratively calculate fuel required
                # On the first iteration it is calculated from module dry mass
                newFuel = required_fuel(newFuel)
                if newFuel <= 0:
                    break
                else:
                    moduleFuel = moduleFuel + newFuel
            fuel = fuel + moduleFuel
    print("\nFinal fuel count: {0}\n".format(fuel))


if __name__ == "__main__":
    main()
