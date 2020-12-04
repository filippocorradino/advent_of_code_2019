#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 15 - Challenge 1
https://adventofcode.com/2019/day/15

Solution: 236

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


from queue import LifoQueue
from aocmodule import Display, Graph, Intcode


screendict = {0: '█',  # block
              1: ' ',  # free tile
              2: 'X',  # target tile
              3: '.',  # planned path
              4: '#',  # open set tile
              5: '!',  # current destination
              6: 'D'}  # current position


def display_status(monitor, environment, path, open_set, goal, current):
    """Display current status

    Pixel states are as follows:
    - 0: block
    - 1: free tile
    - 2: target tile
    - 3: planned path
    - 4: open set tile
    - 5: current destination
    - 6: current position
    """
    monitor.update(environment)
    if path:
        monitor.update({x: 3 for x in path})
    if open_set:
        monitor.update({x: 4 for x in open_set.queue})
    monitor.update({goal: 5})
    monitor.update({current: 6})
    monitor.show()


def neighbours(position):
    return {(position[0], position[1]+1): 1,  # N
            (position[0], position[1]-1): 2,  # S
            (position[0]-1, position[1]): 3,  # W
            (position[0]+1, position[1]): 4}  # E


def create_neighbour_edges(position, environment, pathspace, cost=1):
    current_neighbours = neighbours(position)
    for neighbour in current_neighbours:
        if neighbour in environment and environment[neighbour] != 0:
            pathspace.add_edge(position, neighbour,
                               cost=cost, two_ways=True)


def reconstruct_directions(path):
    directions = []
    for i in range(len(path) - 1):
        directions.append(neighbours(path[i])[path[i+1]])
    return directions


def step(program, direction):
    program.input(direction)
    while not program.iswaiting:
        program.step()
    return program.output()


def survey_area(program, environment, pathspace, current, objective,
                monitor=None):
    if monitor:
        monitor.symbol_dict = screendict
        monitor.default_pixel = 1
    found = False
    open_set = LifoQueue()  # DFS, we assume the search space is bounded...
    while not found:
        # Add new neighbours to open set (we assume they are all traversable)
        current_neighbours = neighbours(current)
        for neighbour in current_neighbours:
            if neighbour not in environment and \
               neighbour not in (x for x in open_set.queue):
                open_set.put(neighbour)
                pathspace.add_node(neighbour)
                # Add edges to all known nodes contiguous to this neighbour
                create_neighbour_edges(neighbour, environment, pathspace)
        # Find path to the oldest node added to the open set
        if open_set.qsize():
            goal = open_set.get()
        else:
            break  # Completed survey
        path = \
            pathspace.a_star(current, goal,
                             lambda x: abs(x[0]-goal[0]) + abs(x[1]-goal[1]))
        directions = reconstruct_directions(path)
        if monitor:
            display_status(monitor, environment, path, open_set, goal, current)
        # Try to reach said node
        while directions:
            program.input(directions.pop(0))
            program.step()  # Ingest input so that iswaiting is cleared
            while not program.iswaiting:
                program.step()
            status = program.output()
        # Update knowledge
        environment[path[-1]] = status
        if status == 0:
            # Last step we hit a wall
            current = path[-2]
            pathspace.remove_node(path[-1])
        else:
            # We hit a free cell
            current = path[-1]
        if status == objective:
            # We hit the target tile!
            found = True
    return current


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
    current = survey_area(program, environment, pathspace, current,
                          objective=2, monitor=monitor)
    path = pathspace.a_star(start, current,
                            lambda x: (abs(x[0]-current[0]) +
                                       abs(x[1]-current[1])))
    n_moves = len(path) - 1
    print("\nMinimum number of moves: {0}\n".format(n_moves))
    return n_moves


if __name__ == "__main__":
    main(display=True)
