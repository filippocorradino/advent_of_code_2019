#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 13 - Challenge 2
https://adventofcode.com/2019/day/13

Solution: 12954

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

import os
from aocmodule import Intcode


screendict = {0: ' ',
              1: '█',
              2: '#',
              3: '=',
              4: 'O'}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_screen(screen, score):
    max_x = max((x for (x, y) in screen))
    max_y = max((y for (x, y) in screen))
    # Reconstruct all panel values
    rows = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            try:
                row.append(screen[(x, y)])
            except KeyError:
                row.append(0)
        rows.append(row)
    # Display
    output = \
        '\n'.join((''.join((screendict[j]) for j in row) for row in rows))
    clear()
    print("\n{0}\nSCORE: {1}\n".format(output, score))
    return output


def main(display=False):
    screen = {}
    program = Intcode()
    program.load_from_file('inputs/day_13_input.txt')
    program.memory.update({0: 2})  # Hack to play for free
    x_ball = None
    x_paddle = None
    score = 0
    joystick = 0
    while not program.ishalted:
        while not program.iswaiting and not program.ishalted:
            program.step()
        while program.output_buffer:
            x = program.output()
            y = program.output()
            v = program.output()
            if x == -1 and y == 0:
                score = v
            else:
                if v == 3:
                    x_paddle = x
                if v == 4:
                    x_ball = x
            screen.update({(x, y): v})
        if (x_ball is not None) and (x_paddle is not None):
            joystick = (x_ball > x_paddle) - (x_ball < x_paddle)
            program.input(joystick)
            program.step()  # Clear the waiting condition
        if display:
            display_screen(screen, score)
    print("\nFinal score: {0}\n".format(score))
    return score


if __name__ == "__main__":
    main()
