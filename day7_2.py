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

import itertools
from aocmodule import Intnetwork


def main():
    amps = ('Amp A', 'Amp B', 'Amp C', 'Amp D', 'Amp E')
    ports = ('INPUT', 'THRUSTER')
    ampli_circuit = Intnetwork()
    ampli_circuit.add_nodes(amps)
    ampli_circuit.add_ports(ports)
    ampli_circuit.add_pipe('INPUT', 'Amp A')
    ampli_circuit.add_pipe('Amp A', 'Amp B')
    ampli_circuit.add_pipe('Amp B', 'Amp C')
    ampli_circuit.add_pipe('Amp C', 'Amp D')
    ampli_circuit.add_pipe('Amp D', 'Amp E')
    ampli_circuit.add_pipe('Amp E', 'THRUSTER')
    ampli_circuit.add_pipe('Amp E', 'Amp A')

    max_signal = None
    for sequence in list(itertools.permutations(list(range(5, 10)))):
        ampli_circuit.clear_buffers(amps)
        ampli_circuit.clear_buffers(ports)
        i_node = 0
        for amp in amps:
            ampli_circuit.nodes[amp].load_from_file('inputs/day_7_input.txt')
            ampli_circuit.nodes[amp].input(sequence[i_node])
            i_node = i_node + 1
        ampli_circuit.nodes['INPUT'].input(0)
        ampli_circuit.execute()
        signal = ampli_circuit.nodes['THRUSTER'].output_buffer[-1]  # Last value
        if max_signal is None or signal > max_signal:
            max_signal = signal
            best_sequence = sequence

    print("\nMaximum achievable signal is {0}, with phase settings {1}\n"
          .format(max_signal, best_sequence))
    return max_signal


if __name__ == "__main__":
    main()
