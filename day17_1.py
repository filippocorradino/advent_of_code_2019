#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 17 - Challenge 1
https://adventofcode.com/2019/day/17

Solution: 2804

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


from aocmodule import Intcode


def map_scaffolding():
    program = Intcode()
    program.load_from_file('inputs/day_17_input.txt')
    program.execute()
    output = program.output_buffer
    outstr = ''.join(chr(x) for x in output)
    lines = outstr.split('\n')
    lines = [line for line in lines if line]
    return lines


def main():
    lines = map_scaffolding()
    calibration_total = 0
    for i_row in range(1, len(lines)-1):
        for i_col in range(1, len(lines[i_row])-1):
            if (lines[i_row][i_col] == '#'
               and lines[i_row-1][i_col] == '#'
               and lines[i_row+1][i_col] == '#'
               and lines[i_row][i_col-1] == '#'
               and lines[i_row][i_col+1] == '#'):
                calibration_total = calibration_total + (i_row * i_col)
    print("\nCalibration parameter: {0}\n".format(calibration_total))
    return calibration_total


if __name__ == "__main__":
    main()
