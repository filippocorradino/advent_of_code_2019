#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 17 - Challenge 2
https://adventofcode.com/2019/day/17

Solution: 833429

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


import re
from collections import deque
from copy import deepcopy
from aocmodule import Intcode, Display, replace_sublist, split_list
from day17_1 import map_scaffolding


def _compress_recursion(commands, symbols, maxlen):
    """
    Recursive support function for the compress() function below
    It tries to find a dictionary of subsequences (i.e. "Functions" in the
    input text) with the provided symbols as key, such that all the commands
    sequence can be mapped.
    Each Function needs to be less than maxlen characters when formatted as the
    problem required.
    Returns None, or the dictionary of symbols if a solution was found.
    """
    # Base Case
    if not symbols:
        if not commands:
            # After all substitutions nothing was left, valid!
            return {}
        else:
            # Still some leftovers, invalid
            return None
    # Recursive Case
    for n_sub in range(1, len(commands[0])+1):
        # Pick a test subsequence in the first command sequence "fragment"
        subsequence = commands[0][:n_sub]
        if len(','.join(subsequence)) > maxlen:
            continue
        # Replace it in all the fragments (but preserve the original)
        commands_sub = deepcopy(commands)
        for part in commands_sub:
            replace_sublist(part, subsequence, [symbols[0]])
        # Split all in further fragments using the new symbol as separator
        commands_split = []
        for part in commands_sub:
            commands_split = commands_split + \
                [x for x in split_list(part, [symbols[0]]) if x]
        # Recursion with the newly fragmented list and the next symbol
        dictionary = _compress_recursion(commands_split, symbols[1:], maxlen)
        if dictionary is not None:
            dictionary[symbols[0]] = subsequence
            return dictionary
    return None


def compress(commands, symbols, maxlen):
    """
    We make some strong assumptions on the commands sequence and its
    compression. In particular, we assume that subsequences for the dictionary
    compression (i.e. "Functions" in the input text) don't split movements in
    half.
    We have to receive commands as a list and not a string, which sucks, but
    otherwise we'd risk splitting the numbers (e.g. ...L12... --> ...L1 2...)
    We're going to explicitly brute force through possible Functions A, B, C.
    I tried using Sequitur but it just couldn't get to the answer
    """
    listfunctions = _compress_recursion([commands], symbols, maxlen)
    if listfunctions is None:
        return None
    functions = {}
    for symbol, listfunction in listfunctions.items():
        replace_sublist(commands, listfunction, [symbol])
        functions[symbol] = ','.join(listfunction)
    sequence = ','.join(commands)
    if len(sequence) < maxlen:
        # We found a solution
        return sequence, functions
    return None


def main(display=False):
    """
    We'll only use LEFT rotations, since R = LLL, so we'll recover it later.

    We'll also work with the map spread out on a single line
    In this configuration, L-R is -/+ 1 and U-D is -/+ N, (N is a line length)

    First we trace the scaffold with the strategy "keep going forward until you
    can only turn, then turn - all until you can only backtrack".
    Then we try to compress the obtained command sequence, and give the result
    to the Intcode computer to process.
    """
    # Prepare the map
    lines = map_scaffolding()
    N = len(lines[0])
    mapstr = ''.join(lines)

    # Circular list with main directions in CW order (Up Right Down Left)
    directions = deque([-N, +1, +N, -1])

    def turn_left():
        directions.rotate(+1)  # This "rotates the robot"

    def front():
        return directions[0]  # This indicates "the direction the robot faces"

    def next_tile(position, last_visited):
        """
        Returns true if the tile in front of the robot is a valid scaffold tile
        We make sure that it's not a recently visited scaffold, so we're not
        just backtracking, hence the "valid"
        """
        try:
            new_position = position + front()
            if mapstr[new_position] == '#' and new_position != last_visited:
                # Also check that we're not crossing the L or R borders
                if not (((position % N) == 0 and front() == -1) or
                        ((position % N) == N-1 and front() == +1)):
                    return True
        except IndexError:
            pass
        return False

    # PATHFINDING & COMMAND BUILDING
    # Find the robot
    robot_pos = re.search(r'[^\.\#]', mapstr).start()
    last_visited = None
    robot_dir = {'^': -N, '>': +1, 'v': +N, '<': -1}[mapstr[robot_pos]]
    # Align reference system, since front() by default is pointing Up
    while front() != robot_dir:
        turn_left()
    # Build command sequence as a list
    commands = []
    while True:
        rotation_timeout = 0
        while not next_tile(robot_pos, last_visited) and rotation_timeout < 4:
            turn_left()
            commands.append('L')
            rotation_timeout = rotation_timeout + 1
        if rotation_timeout == 4:
            break  # We're spinning in circles, nowhere left to go...
        counter = 0
        while next_tile(robot_pos, last_visited):
            last_visited = robot_pos
            robot_pos = robot_pos + front()
            counter = counter + 1
        commands.append(str(counter))
    # Cut away last Ls while spinning in cicles and convert LLL into R
    while commands[-1] == 'L':
        commands.pop(-1)
    replace_sublist(commands, ['L', 'L', 'L'], ['R'])
    # Compress commands
    symbols = ['A', 'B', 'C']
    sequence, functions = compress(commands, symbols, maxlen=20)

    # RUNNING THE INTCODE PROGRAM
    program = Intcode()
    program.load_from_file('inputs/day_17_input.txt')
    program.memory[0] = 2  # Manual override
    video_feed = {True: 'y', False: 'n'}[display]
    # Build program input
    program_input = '{0}\n'.format(sequence)
    for s in symbols:
        program_input = program_input + '{0}\n'.format(functions[s])
    program_input = program_input + '{0}\n'.format(video_feed)
    for x in program_input:
        program.input(ord(x))
    # Run the program
    if display:
        # Live video feed
        screen_buffer = ''
        while not program.ishalted:
            program.step()
            if program.output_buffer:
                screen_buffer += chr(program.output())
                # TODO: handle values outside of chr range
            if screen_buffer[-2:] == '\n\n':
                Display.clear()
                print(screen_buffer, end='')
                screen_buffer = ''
        dust = ord(screen_buffer[-1])  # Reconstruct dust from last output
    else:
        # Output only
        program.execute()
        dust = program.output_buffer[-1]
    # Output
    print("\nFound a solution with sequence: {0}".format(sequence))
    for symbol in symbols:
        print("{0}: {1}".format(symbol, functions[symbol]))
    print("\nTotal dust collected: {0}\n".format(dust))
    return dust


if __name__ == "__main__":
    main(display=True)
