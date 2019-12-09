#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 6 - Challenge 2
https://adventofcode.com/2019/day/6

Solution: 382

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Orbiter
from day6_1 import import_orbitmap


def main():
    bodies = import_orbitmap()
    # Get list of parents from body to COM
    chain_you = bodies['YOU'].get_chain()
    chain_san = bodies['SAN'].get_chain()
    # Prune away common ancestors to find last common parent
    while chain_san[-1] == chain_you[-1]:
        chain_san.pop()
        chain_you.pop()
    # Up/Down one chain = len(chain) - 1
    # Across chains with common originator (popped) = 2
    transfers = len(chain_san) + len(chain_you)
    print("\nMinimum number of transfers is: {0}\n".format(transfers))
    return transfers


if __name__ == "__main__":
    main()
