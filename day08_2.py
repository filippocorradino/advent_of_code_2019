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
    colour_dict = {'0': '█',  # Black block
                   '1': ' '}   # White space
    width = 25
    height = 6
    layers = list(get_picture_layers('inputs/day_08_input.txt', width, height))
    merger = \
        ''.join(colour_dict[next(colour for colour in pixel if colour != '2')]
                for pixel in zip(*layers))
    output = '\n'.join(chunk_string(merger, width))
    print(output)
    return output


if __name__ == "__main__":
    main()
