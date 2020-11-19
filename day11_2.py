#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 11 - Challenge 2
https://adventofcode.com/2019/day/11

Solution: LBJHEKLH

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from day11_1 import paint_hull


def main():
    hull = {(0, 0): 1}  # Dictionary of panel coordinates: 0 = black, 1 = white
    coordinates = (0, 0)  # Starting coordinates (white panel in hull)
    hull, _ = paint_hull(hull, coordinates)
    # Get borders
    min_x = min((x for (x, y) in hull))
    max_x = max((x for (x, y) in hull))
    min_y = min((y for (x, y) in hull))
    max_y = max((y for (x, y) in hull))
    # Reconstruct all panel values
    rows = []
    for y in range(max_y, min_y-1, -1):
        row = []
        for x in range(min_x, max_x+1):
            try:
                row.append(hull[(x, y)])
            except KeyError:
                row.append(0)
        rows.append(row)
    # Display
    colour_dict = {0: '█',  # Black block
                   1: ' '}  # White space
    output = \
        '\n'.join((''.join((colour_dict[j]) for j in row) for row in rows))
    print('\n' + output + '\n')
    return output


if __name__ == "__main__":
    main()
