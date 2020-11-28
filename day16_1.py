#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 16 - Challenge 1
https://adventofcode.com/2019/day/16

Solution: 19944447

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


def precalculate_pattern(n_data, pattern):
    full_pattern = []
    P = len(pattern)
    for k in range(n_data):  # output digit index
        pattern_line = []
        for ix in range(n_data):  # input digit index
            ip = ((ix+1) // (k+1)) % P  # creates proper patter for the digit
            pattern_line.append(pattern[ip])
        full_pattern.append(pattern_line)
    return full_pattern


def fft_phase(data, full_pattern):
    output = []
    N = len(data)
    for k in range(N):  # output digit index
        # |sum data[i]*pattern[i]| % 10
        output.append(
            abs(sum(x*y for (x, y) in zip(data, full_pattern[k]))) % 10)
    return output


def main(n_phases=100):
    data = []
    with open('inputs/day_16_input.txt') as file:
        for digit in file.read():
            data.append(int(digit))
    full_pattern = precalculate_pattern(len(data), [0, 1, 0, -1])
    for _ in range(n_phases):
        data = fft_phase(data, full_pattern)
    datastring = ''.join(str(x) for x in data[:8])
    print("\nPattern after {0} FFT phases: {1}...\n"
          .format(n_phases, datastring))
    return int(datastring)


if __name__ == "__main__":
    main()
