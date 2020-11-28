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

from aocmodule import Intcode, Display


screendict = {0: ' ',
              1: '█',
              2: '#',
              3: '=',
              4: 'O'}


def main(display=False):
    program = Intcode()
    program.load_from_file('inputs/day_13_input.txt')
    program.memory[0] = 2  # Hack to play for free
    x_ball = None
    x_paddle = None
    score = 0
    joystick = 0
    monitor = Display(screendict)
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
                monitor.update({(x, y): v})
        if (x_ball is not None) and (x_paddle is not None):
            joystick = (x_ball > x_paddle) - (x_ball < x_paddle)
            program.input(joystick)
            program.step()  # Clear the waiting condition
        if display:
            monitor.show(legend='SCORE: {0}'.format(score))
    print("\nFinal score: {0}\n".format(score))
    return score


if __name__ == "__main__":
    main(display=True)
