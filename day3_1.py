#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 3 - Challenge 1
https://adventofcode.com/2019/day/3

Solution: 1285

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


def main():
    """ The idea is to create a dictionary with the following items:
        (x, y): {wireID: weight, ...}
        for each point (x, y) touched by at least one wire.
        The length of the {wireID: weight, ...} dict gives info on overlaps
        The weight field can store other useful information to filter overlaps
    """
    stepMap = {'U': (0, +1),
               'D': (0, -1),
               'L': (-1, 0),
               'R': (+1, 0)}
    with open('inputs/day_3_input.txt') as file:
        wiring = {}
        wireID = 0
        for line in file:
            wire = {}
            wireID = wireID + 1
            point = (0, 0)
            for segment in line.split(','):
                # Format of segment is DXXX, with D = U/D/L/R
                step = stepMap[segment[0]]
                for _ in range(0, int(segment[1:])):
                    # Ignore point at (0, 0)
                    point = tuple(x+y for x, y in zip(point, step))
                    entry = {wireID: 0}  # No weight required
                    if point not in wiring:
                        if point not in wire:
                            wire.update({point: entry})
                    else:
                        wiring[point].update(entry)
            wiring.update(wire)
    # Find overlaps and filter them
    overlaps = [sum(abs(x) for x in point)
                for point in wiring if len(wiring[point]) > 1]
    answer = min(overlaps)
    print("\nMinimum distance: {0}\n".format(answer))
    return answer


if __name__ == "__main__":
    main()
