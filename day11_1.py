#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 11 - Challenge 1
https://adventofcode.com/2019/day/11

Solution: 2021

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from collections import deque
from aocmodule import Intcode


def advance(coordinates, direction):
    # Move one step in the given direction
    new_coordinates = ()
    for x, dx in zip(coordinates, direction):
        new_coordinates = new_coordinates + (x + dx,)
    return new_coordinates


def paint_hull(hull, coordinates):
    # Circular list with main directions in a cartesian frame (CW order)
    # Default (starting) direction is the first, to the North
    directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])

    def turn_left():
        directions.rotate(1)

    def turn_right():
        directions.rotate(-1)

    def direction():
        return directions[0]

    program = Intcode()
    program.load_from_file('inputs/day_11_input.txt')
    while True:
        # Provide panel color as input
        try:
            program.input(hull[coordinates])
        except KeyError:
            program.input(0)  # All panels start black
        # Let's wait for the two outputs
        while (len(program.output_buffer) < 2) and not program.ishalted:
            program.step()
        if program.ishalted:
            break
        # First output is the colour
        colour = program.output()
        hull[coordinates] = colour
        # Second output is the rotation
        rotation = program.output()
        if rotation == 0:
            turn_left()
        elif rotation == 1:
            turn_right()
        else:
            raise ValueError()
        coordinates = advance(coordinates, direction())
    return hull, coordinates


def main():
    hull = {}  # Dictionary of panel coordinates with 0 = black, 1 = white
    coordinates = (0, 0)  # Starting coordinates
    hull, _ = paint_hull(hull, coordinates)
    result = len(hull)
    print("\nTotal number of painted panels: {0}\n".format(result))
    return result


if __name__ == "__main__":
    main()
