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
    """
    The idea with this one is that for digits in the second half of the data,
    using the standard pattern, there is a simplified formula for a FFT phase:
    data[k] = abs(sum(data[k:])) % 10
    This is because all pattern values with index 1..k-1 are 0, and then there
    are only 1s for the remainder of the data (doesn't have space to roll over
    to the second zero section).
    Therefore this solution ONLY works if the message lies in the second half
    of the data...
    """
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
