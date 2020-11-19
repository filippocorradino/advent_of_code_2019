#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 12 - Challenge 2
https://adventofcode.com/2019/day/12

Solution: 332477126821644

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from math import gcd
from aocmodule import LunarSystem


def lcm(numbers):
    # Least common multiplier
    lcm = 1
    for number in numbers:
        lcm = (lcm * number) // gcd(lcm, number)
    return lcm


def main():
    system = LunarSystem.import_moons('inputs/day_12_input.txt')
    cycles = []
    for axis in [0, 1, 2]:
        phase_space = {}
        current_state = str(system.state_vector_1d(axis))
        counter = 0
        while current_state not in phase_space:
            phase_space.update({current_state: counter})
            counter = counter + 1
            system.propagate()
            current_state = str(system.state_vector_1d(axis))
        pre_existing = phase_space[current_state]
        # print("Found a recurring state in {0} axis: ".format('XYZ'[axis]),
        #       end="")
        # print("step {0} is repeated after {1} cycles"
        #       .format(pre_existing, counter))
        if pre_existing == 0:
            cycles.append(counter)
        else:
            raise RuntimeError("Loops are out of phase at start condition")
    total_cycle = lcm(cycles)
    print("\nMinimum cycles for a recurring state in X, Y, Z: {0}\n"
          .format(total_cycle))
    return total_cycle


if __name__ == "__main__":
    main()
