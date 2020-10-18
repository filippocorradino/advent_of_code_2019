#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 10 - Challenge 2
https://adventofcode.com/2019/day/10

Solution: 815

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from collections import namedtuple
from math import atan2, sqrt, pi
from day10_1 import get_asteroid_map
from day10_1 import main as previous_solution


Asteroid = namedtuple('Asteroid', ('coords', 'angle', 'range'))


def angle(target, center):
    angle = atan2(target[1]-center[1], target[0]-center[0])
    # Our x axis is right and y axis is down, so angles are:
    # 000 RIGHT - 090 DOWN  - 180 LEFT  - 270 UP
    # We actually want clockwise angles from -y
    # 000 UP    - 090 RIGHT - 180 DOWN  - 270 LEFT
    angle = angle + pi/2
    # Wrap angle to 0-2*pi
    while angle < 0:
        angle = angle + 2*pi
    while angle > 2*pi:
        angle = angle - 2*pi
    return angle


def distance(target, center):
    dist = sqrt(pow(target[0]-center[0], 2) + pow(target[1]-center[1], 2))
    return dist


def main():
    laser_coords = previous_solution(get_coords=True, printout=False)
    asteroid_map = get_asteroid_map()
    asteroid_list = [Asteroid(x,
                              angle(x, laser_coords),
                              distance(x, laser_coords))
                     for x in asteroid_map]
    # Sort asteroids by angle and then range
    target_list = sorted(asteroid_list,
                         key=lambda x: (x.angle, x.range))
    # Vaporize the asteroids
    index = 0
    vaporized = 0
    old_angle = None
    while target_list:
        if old_angle == target_list[index].angle:
            # Was behind last target, skip
            index = index + 1
        else:
            # Vaporize the asteroid
            if vaporized == 199:
                break
            old_angle = target_list[index].angle
            target_list.pop(index)
            vaporized = vaporized + 1
        if index == len(target_list):
            # We reached the end of the list, start over
            index = 0
    # Found the 200th vaporized asteroid
    bet_coords = target_list[index].coords
    output = 100*bet_coords[0] + bet_coords[1]
    print("\nThe 200th asteroid to be vaporized is at: {0}"
          "\nWith problem output {1}\n"
          .format(bet_coords, output))
    return output


if __name__ == "__main__":
    main()
