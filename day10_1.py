#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 10 - Challenge 1
https://adventofcode.com/2019/day/10

Solution: 253

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from math import atan2


def get_asteroid_map():
    asteroid_map = []
    with open('inputs/day_10_input.txt') as file:
        y = 0
        for line in file:
            x = 0
            for position in line:
                if position == '#':
                    asteroid_map.append((x, y))
                x = x + 1
            y = y + 1
    return asteroid_map


def main(get_coords=False, printout=True):
    asteroid_map = get_asteroid_map()
    # Find best asteroid for the station
    best_candidate = (0, 0)
    best_value = 0
    for candidate_station in asteroid_map:
        angles_list = []
        for target in asteroid_map:
            if target is not candidate_station:
                view_angle = atan2(target[1]-candidate_station[1],
                                   target[0]-candidate_station[0])
                if view_angle not in angles_list:
                    angles_list.append(view_angle)
        if len(angles_list) > best_value:
            best_candidate = candidate_station
            best_value = len(angles_list)
    if printout:
        print("\nBest placement for monitoring station is: {0}"
              "\nWith {1} asteroids in view\n"
              .format(best_candidate, best_value))
    if get_coords:
        return best_candidate
    else:
        return best_value


if __name__ == "__main__":
    main()
