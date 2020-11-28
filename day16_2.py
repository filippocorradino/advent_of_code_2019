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


def cheaty_fft_phase(data):
    output = data.copy()
    total = sum(data)
    for k in range(len(data)):
        output[k] = abs(total) % 10
        total = total - data[k]
    return output


def main(n_phases=100, repeat=10000, message_len=8, offset_indicator_len=7):
    data = []
    with open('inputs/day_16_input.txt') as file:
        for digit in file.read():
            data.append(int(digit))
    data = data * repeat
    start_index = int(''.join(str(x) for x in data[:offset_indicator_len]))
    if start_index < (len(data) // 2) or start_index + message_len > len(data):
        raise RuntimeError("I surrender!")
    data = data[start_index:]
    for k in range(n_phases):
        data = cheaty_fft_phase(data)
    datastring = ''.join(str(x) for x in data[:message_len])
    print("\nMessage extracted after {0} FFT phases: {1}\n"
          .format(n_phases, datastring))
    return int(datastring)


if __name__ == "__main__":
    main()
