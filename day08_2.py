#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 8 - Challenge 2
https://adventofcode.com/2019/day/8

Solution: PFCAK

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from day08_1 import chunk_string, get_picture_layers


def main():
    color_dict = {'0': '█',  # Black block
                  '1': ' '}   # White space
    width = 25
    height = 6
    layers = list(get_picture_layers('inputs/day_08_input.txt', width, height))
    merger = \
        ''.join(next(colour for colour in pixel if colour is not '2')
                for pixel in zip(*layers))
    rows = chunk_string(merger, width)
    for row in rows:
        print(''.join(color_dict[pixel] for pixel in row))
    print(merger)
    return merger


if __name__ == "__main__":
    main()
