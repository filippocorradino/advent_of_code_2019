#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 15 - Challenge 2
https://adventofcode.com/2019/day/15

Solution: 368

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


from day15_1 import survey_area
from aocmodule import Display, Graph, Intcode


screendict = {0: '█',
              1: ' ',
              2: 'O'}


def main(start=(0, 0), display=False):
    if display:
        monitor = Display()
    else:
        monitor = None
    program = Intcode()
    program.load_from_file('inputs/day_15_input.txt')
    current = start
    environment = {current: 1}
    pathspace = Graph(nodes=[current])
    # Survey all compartment
    survey_area(program, environment, pathspace, current,
                objective=None, monitor=monitor)
    # Now diffuse the oxygen
    if display:
        monitor.symbol_dict = screendict
        monitor.default_pixel = 1
    minute = -1
    open_oxygen_set = \
        [next(coordinates for coordinates, value in environment.items()
              if value == 2)]  # Only oxygen generator for now
    while open_oxygen_set:
        minute = minute + 1
        for x in open_oxygen_set:
            environment[x] = 2
        if display:
            monitor.refresh(environment, legend="MINUTE {0}".format(minute))
        # Update open set with all adjacent tiles (not yet oxygenated)
        open_oxygen_set = [x[1] for x in pathspace.edges if
                           x[0] in open_oxygen_set and environment[x[1]] == 1]
    print("\nOxygen will fill the compartment in: {0} minutes\n"
          .format(minute))
    return minute


if __name__ == "__main__":
    main(display=True)
