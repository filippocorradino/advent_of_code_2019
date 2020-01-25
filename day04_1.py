#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 4 - Challenge 1
https://adventofcode.com/2019/day/4

Solution: 1063

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


MINPASS = 246540
MAXPASS = 787419


def main():
    possible_passwords = 0

    for password in range(MINPASS, MAXPASS+1):
        digits = [int(d) for d in str(password)]
        digits_diff = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        # Criterion 1: non-decreasing
        criterion1 = all(d >= 0 for d in digits_diff)
        # Criterion 2: at least two repeating digits
        criterion2 = 0 in digits_diff
        #
        if criterion1 and criterion2:
            possible_passwords = possible_passwords + 1

    print("\nPossible passwords: {0}\n".format(possible_passwords))
    return possible_passwords


if __name__ == "__main__":
    main()
