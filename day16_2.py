#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 16 - Challenge 2
https://adventofcode.com/2019/day/16

Solution: 81207421
Really not proud of this one...

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


def cheaty_fft_phase(data, start_index):
    output = data.copy()
    total = sum(data[start_index-1:])
    for k in range(start_index, len(data)):
        total = total - data[k-1]
        output[k] = abs(total) % 10
    return output


def main(n_phases=100, repeat=1000, message_len=8, offset_indicator_len=7):
    data = []
    with open('inputs/day_16_input.txt') as file:
        for digit in file.read():
            data.append(int(digit))
    data = data*10000
    start_index = int(''.join(str(x) for x in data[:offset_indicator_len]))
    if start_index < (len(data) // 2) or start_index + message_len > len(data):
        raise RuntimeError("I surrender!")
    for k in range(n_phases):
        data = cheaty_fft_phase(data, start_index)
    end_index = start_index + message_len
    datastring = ''.join(str(x) for x in data[start_index:end_index])
    print("\nMessage extracted after {0} FFT phases: {1}\n"
          .format(n_phases, datastring))
    return int(datastring)


if __name__ == "__main__":
    main()
