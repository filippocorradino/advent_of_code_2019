#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 7 - Challenge 2
https://adventofcode.com/2019/day/7

Solution: 39016654

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

from aocmodule import Intcode, Intnetwork
import itertools


def main():
    amps = ('Amp A', 'Amp B', 'Amp C', 'Amp D', 'Amp E')
    ports = ('INPUT', 'THRUSTER')
    ampliCircuit = Intnetwork()
    ampliCircuit.add_nodes(amps)
    ampliCircuit.add_ports(ports)
    ampliCircuit.add_pipe('INPUT', 'Amp A')
    ampliCircuit.add_pipe('Amp A', 'Amp B')
    ampliCircuit.add_pipe('Amp B', 'Amp C')
    ampliCircuit.add_pipe('Amp C', 'Amp D')
    ampliCircuit.add_pipe('Amp D', 'Amp E')
    ampliCircuit.add_pipe('Amp E', 'THRUSTER')
    ampliCircuit.add_pipe('Amp E', 'Amp A')

    maxSignal = None
    for sequence in list(itertools.permutations(list(range(5, 10)))):
        ampliCircuit.clear_buffers(amps)
        ampliCircuit.clear_buffers(ports)
        iNode = 0
        for amp in amps:
            ampliCircuit.nodes[amp].load_from_file('inputs/day_7_input.txt')
            ampliCircuit.nodes[amp].input(sequence[iNode])
            iNode = iNode + 1
        ampliCircuit.nodes['INPUT'].input(0)
        ampliCircuit.execute()
        signal = ampliCircuit.nodes['THRUSTER'].outputBuffer[-1]  # Last value
        if maxSignal is None or signal > maxSignal:
            maxSignal = signal
            bestSequence = sequence

    print("\nMaximum achievable signal is {0}, with phase settings {1}\n"
          .format(maxSignal, bestSequence))
    return maxSignal


if __name__ == "__main__":
    main()
