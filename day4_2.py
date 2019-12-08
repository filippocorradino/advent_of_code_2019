#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 4 - Challenge 2
https://adventofcode.com/2019/day/4

Solution: 686

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from collections import Counter


MINPASS = 246540
MAXPASS = 787419


def main():
    possiblePasswords = 0

    for password in range(MINPASS, MAXPASS+1):
        digits = [int(d) for d in str(password)]
        digitsDiff = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        # Criterion 1: non-decreasing
        criterion1 = all(d >= 0 for d in digitsDiff)
        # Criterion 2: at least once exactly two repeating digits
        criterion2 = 2 in Counter(digits).values()
        #
        if criterion1 and criterion2:
            possiblePasswords = possiblePasswords + 1

    print("\nPossible passwords: {0}\n".format(possiblePasswords))
    return possiblePasswords


if __name__ == "__main__":
    main()
