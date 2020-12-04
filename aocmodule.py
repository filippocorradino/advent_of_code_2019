"""
Advent of Code 2019 - Utilities Module
https://adventofcode.com/2019/

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

import itertools
import heapq
import math
import os
import re


class Intcode():

    def __init__(self, state=[]):
        self.memory = {}
        self.load(state)
        self.clear_buffers()

    # State loading and setting methods

    def load(self, state, ip=0, clearBuffers=False):
        """Load a program

        Loads a program into memory and sets the Instruction Pointer.

        Args:
            state (list):
                The program listing as a list of ints.
            ip (int):
                The value to be assigned to the Instruction Pointer.
        """
        # TODO: understand why the following alternative doesn't work:
        # self.memory.update({i: e for (i, e) in enumerate(state)})
        for position in range(len(state)):
            self.memory.update({position: state[position]})
        self.ip = ip
        self.relative_base = 0
        self.original = self.memory.copy()  # Save a static copy
        # Reset status flags
        self.iswaiting = False
        self.ishalted = False
        if clearBuffers:
            self.clear_buffers()

    def load_from_file(self, file, ip=0):
        """Load a program from file

        Loads a program from file into memory and sets the Instruction Pointer.

        Args:
            file (str):
                Path of the text file containing the program listing.
            ip (int):
                The value to be assigned to the Instruction Pointer.
        """
        with open(file) as source:
            state = []
            for line in source:
                state = state + [int(item) for item in line.split(',')]
        self.load(state, ip)

    def rewind(self):
        """Rewind program

        Reverts execution to the last program load operation.
        """
        self.load(self.original)

    def clear_buffers(self):
        """Clear I/O buffers

        Clears both input and output buffers.
        """
        self.input_buffer = []
        self.output_buffer = []

    # I/O methods

    def _fetch(self, address):
        """Fetch a value from memory

        Fetches a value from memory at a given address.
        If the address is not yet recorded, it is added, then its value
        initialized to 0, and the method returns 0.

        Args:
            address (int):
                The memory address.

        Returns:
            value (int):
                The value stored at the given address.
        """
        if address not in self.memory:
            self.memory[address] = 0
        value = self.memory[address]
        return value

    def _store(self, address, value):
        """Writes a value to memory

        Writes a value to memory at a given address.
        If the address is not yet recorded, it is added, then its value is
        written.

        Args:
            address (int):
                The memory address.
            value (int):
                The value to be stored at the given address.
        """
        self.memory[address] = value

    def dsky(self, noun, verb):
        """DSKY input

        Receives DSKY-like input, i.e. a NOUN and VERB statement.

        Args:
            noun (int):
                NOUN part of the statement, goes to memory[1].
            verb (int):
                VERB part of the statement, goes to memory[2].
        """
        self._store(1, noun)
        self._store(2, verb)

    def input(self, value):
        """General input

        Args:
            value (int):
                Numeric input to be pushed into the input buffer.
        """
        self.input_buffer.append(value)

    def output(self):
        """General output

        Returns:
            output (int):
                Oldest item in the output buffer.
        """
        if self.output_buffer:
            output = self.output_buffer.pop(0)
            return output
        else:
            return None

    # Running methods

    def _parse_opcode(self, raw_opcode):
        """Parse raw opcode

        This method receives a raw opcode as read in the program listing,
        and produces the refined opcode (identifying an operation), along with
        the raw information on arguments modes (position/immediate/...)

        Args:
            raw_opcode (int):
                The raw opcode, as read in the program listing.

        Returns:
            opcode (int):
                The refined opcode (no parameters mode info).
            raw_modes (int):
                A number containing parameters mode info.
                In decimal notation, from right to left each digit represents
                the mode of a parameter.
                Leading zeros are omitted in this representation.
        """
        raw_modes, opcode = divmod(raw_opcode, 100)
        return opcode, raw_modes

    def _parse_parameters(self, opcode, raw_modes, n_parameters):
        """Parse instruction parameters

        Given the raw mode information as generated by _parse_opcode and the
        number of parameters accepted by that instruction, it generates a list
        of parameter values for use by the operator.
        A string containing easy-to-access information on parameters modes is
        also generated, should it be required.

        Note:
            By default all current parameters are obtained, even those which
            might actually indicate outputs instead of inputs.

        Args:
            raw_modes (int):
                A number containing parameters mode info.
                In decimal notation, from right to left each digit represents
                the mode of a parameter.
                Leading zeros are omitted in this representation.
            n_parameters (int):
                The number of parameters of the instruction.
                NOT counting the opcode!

        Returns:
            modes (str):
                Each char represents a parameter of the instruction.
                X marks the actual opcode, i.e. [IP]
                0 marks a parameter passed in position mode
                1 marks a parameter passed in immediate mode

            values (list):
                values[0] is the refined opcode (no mode information)
                values[1:] are the other parameters of the instruction

            addresses (list):
                addresses from where the items in values were fetched
        """
        modes = '{0:0{1}d}X'.format(raw_modes, n_parameters)
        modes = modes[::-1]
        values = [opcode]
        addresses = [self.ip]
        for offset in range(1, 1+n_parameters):
            parameter = self._fetch(self.ip+offset)
            mode = modes[offset]
            if mode == '0':
                # Position mode
                address = parameter
            if mode == '1':
                # Immediate mode
                address = self.ip+offset
            if mode == '2':
                # Relative mode
                address = parameter + self.relative_base
            addresses.append(address)
            values.append(self._fetch(address))

        return modes, values, addresses

    def _std_ip_advance(self, n_parameters):
        """Standard Instruction Pointer advance

        Advances the Instruction Pointer to the next instruction.

        Args:
            n_parameters (int):
                Number of parameters of the executed instruction.
                NOT counting the opcode!
        """
        self.ip = self.ip + n_parameters + 1

    def step(self):
        """Program step

        Executes one instruction cycle.
        """
        # Fetch and execute next instruction
        opcode, raw_modes = self._parse_opcode(self._fetch(self.ip))
        if opcode == 1:
            # 3 parameters. MOV [IP+3], (IP+1) + (IP+2)
            n_params = 3
            modes, values, addresses = \
                self._parse_parameters(opcode, raw_modes, n_params)
            assert modes[3] in '02'  # Output always position-like mode
            self._store(addresses[3], values[1] + values[2])
            self._std_ip_advance(n_params)
        if opcode == 2:
            # 3 parameters. MOV [IP+3], (IP+1) * (IP+2)
            n_params = 3
            modes, values, addresses = \
                self._parse_parameters(opcode, raw_modes, n_params)
            assert modes[3] in '02'  # Output always position-like mode
            self._store(addresses[3], values[1] * values[2])
            self._std_ip_advance(n_params)
        if opcode == 3:
            # 1 parameter. MOV [IP+1], IN
            n_params = 1
            modes, values, addresses = \
                self._parse_parameters(opcode, raw_modes, n_params)
            assert modes[1] in '02'  # Save always position-like mode
            if self.input_buffer:  # Input available
                self.iswaiting = False  # Clear waiting condition, if any
                self._store(addresses[1], self.input_buffer.pop(0))
                self._std_ip_advance(n_params)
            else:
                self.iswaiting = True
        if opcode == 4:
            # 1 parameter. MOV OUT, (IP+1)
            n_params = 1
            _, values, _ = self._parse_parameters(opcode, raw_modes, n_params)
            self.output_buffer.append(values[1])
            self._std_ip_advance(n_params)
        if opcode == 5:
            # 2 parameters. JNZ (IP+2)
            n_params = 2
            _, values, _ = self._parse_parameters(opcode, raw_modes, n_params)
            if values[1] != 0:
                self.ip = values[2]
            else:
                self._std_ip_advance(n_params)
        if opcode == 6:
            # 2 parameters. JEZ (IP+2)
            n_params = 2
            _, values, _ = self._parse_parameters(opcode, raw_modes, n_params)
            if values[1] == 0:
                self.ip = values[2]
            else:
                self._std_ip_advance(n_params)
        if opcode == 7:
            # 3 parameters. MOV [IP+3], (IP+1) < (IP+2)
            n_params = 3
            modes, values, addresses = \
                self._parse_parameters(opcode, raw_modes, n_params)
            assert modes[3] in '02'  # Output always position-like mode
            if values[1] < values[2]:
                result = 1
            else:
                result = 0
            self._store(addresses[3], result)
            self._std_ip_advance(n_params)
        if opcode == 8:
            # 3 parameters. MOV [IP+3], (IP+1) == (IP+2)
            n_params = 3
            modes, values, addresses = \
                self._parse_parameters(opcode, raw_modes, n_params)
            assert modes[3] in '02'  # Output always position-like mode
            if values[1] == values[2]:
                result = 1
            else:
                result = 0
            self._store(addresses[3], result)
            self._std_ip_advance(n_params)
        if opcode == 9:
            # 1 parameter. MOV RB, RB + (IP+1)
            n_params = 1
            _, values, _ = self._parse_parameters(opcode, raw_modes, n_params)
            self.relative_base = self.relative_base + values[1]
            self._std_ip_advance(n_params)
        if opcode == 99:
            # 1 parameters. HCF
            self.ishalted = True

    def execute(self):
        """Run the program to completion

        Steps through the program until it halts.
        """
        while not self.ishalted:
            self.step()


class Intnetwork():

    #               0  1  2  3     4  5  6  7
    PORT_PROGRAM = [3, 7, 4, 7, 1106, 0, 0, 0]  # Move IN to OUT
    # MOV [7], IN
    # MOV OUT, [7]
    # JEZ 0

    def __init__(self, nodes={}):
        self.nodes = {}
        self.ports = []
        self.pipes = []
        self.add_nodes(nodes)

    def add_nodes(self, tags):
        """Add a set of Intcode computers

        Args:
            tags (Iterable):
                Tags to refer to the nodes.
        """
        for tag in tags:
            self.nodes[tag] = Intcode()

    def add_ports(self, tags):
        """Add a set of ports (or make some node ports)

        Args:
            tags (Iterable):
                Tags to refer to the ports.
        """
        for tag in tags:
            if tag not in self.nodes:
                self.nodes[tag] = Intcode()
            self.nodes[tag].load(Intnetwork.PORT_PROGRAM)

    def add_pipe(self, source, dest):
        """Add an I/O pipes

        An I/O pipe redirects outputs from sourcenode to inputs for destnode.
        One value is transferred per step.

        TODO: add support for multiple additions

        Args:
            source (hashable):
                Tag of the source node of the pipe
            dest (hashable):
                Tag of the destination node of the pipe
        """
        for end in (source, dest):
            if all(end not in available
                   for available in (self.nodes, self.ports)):
                raise KeyError("Node is not a valid node/port of the network")
        self.pipes.append((source, dest))

    def clear_buffers(self, targets):
        """Clear buffers

        Clears the buffers of a set of nodes or ports.
        """
        for target in targets:
            if target in self.nodes:
                self.nodes[target].clear_buffers()
            elif target in self.ports:
                self.ports[target].clear_buffers()
            else:
                raise KeyError("Target isn't a valid node/port of the network")

    def step(self):
        """Programs step

        Executes one instruction cycle for each node in the network.
        Also pushes up to one item of data along each I/O pipe.
        Supports multiple pipes connected to a same node, in which case the
        outgoing value is copied over all the pipes.
        """
        for node in self.nodes:
            self.nodes[node].step()
            out_pipes = [pipe for pipe in self.pipes if pipe[0] == node]
            if out_pipes:
                item = self.nodes[node].output()
                if item is not None:
                    for pipe in out_pipes:
                        self.nodes[pipe[1]].input(item)

    def execute(self):
        """Run the programs to completion

        Steps through the programs until all of them halt or are waiting.
        """
        while not all((self.nodes[node].ishalted or self.nodes[node].iswaiting)
                      for node in self.nodes):
            self.step()


class Orbiter():

    def __init__(self, atlas, main=None):
        self.atlas = atlas
        self.main = main

    def get_orbits(self):
        if self.main is not None:
            return self.atlas[self.main].get_orbits() + 1
        else:
            return 0

    def get_chain(self):
        if self.main is not None:
            return [self.main] + self.atlas[self.main].get_chain()
        else:
            return []


class Moon():

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def _pot_energy(self):
        return sum(abs(x) for x in self.pos)

    def _kin_energy(self):
        return sum(abs(x) for x in self.vel)

    def tot_energy(self):
        return self._pot_energy() * self._kin_energy()


class LunarSystem():

    def __init__(self, moons=[]):
        self.moons = moons

    @classmethod
    def import_moons(cls, infile):
        moons = []
        regex = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'
        with open(infile) as file:
            for line in file:
                moons.append(
                    Moon(pos=[int(x) for x in re.findall(regex, line)[0]],
                         vel=[0, 0, 0]))
        return cls(moons)

    def propagate(self, steps=1):
        """Propagate moons trajectories

        Sign and vector sum functions computed inline for performance
        """
        for k in range(steps):
            for moon_a, moon_b in itertools.combinations(self.moons, r=2):
                r_ab = [b - a for (a, b) in zip(moon_a.pos, moon_b.pos)]
                f_ab = [(x > 0) - (x < 0) for x in r_ab]  # "force" by b on a
                f_ba = [(x < 0) - (x > 0) for x in r_ab]  # "force" by a on b
                moon_a.vel = [v + f for (v, f) in zip(moon_a.vel, f_ab)]
                moon_b.vel = [v + f for (v, f) in zip(moon_b.vel, f_ba)]
            for moon in self.moons:
                moon.pos = [p + v for (p, v) in zip(moon.pos, moon.vel)]

    def total_energy(self):
        return sum(moon.tot_energy() for moon in self.moons)

    def state_vector_1d(self, axis):
        return [(moon.pos[axis], moon.vel[axis]) for moon in self.moons]


class Display():

    def __init__(self, symbol_dict={}, default_pixel=0):
        self.symbol_dict = symbol_dict
        self.default_pixel = default_pixel
        self.pixels = {}
        self.size = None

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def set_size(self, size):
        self.size = size

    def update(self, pixels):
        self.pixels.update(pixels)

    def show(self, legend='', clear=True):
        min_x = min((x for (x, y) in self.pixels))
        min_y = min((y for (x, y) in self.pixels))
        if self.size:
            max_x = min_x + self.size[0]
            max_y = min_y + self.size[1]
        else:
            max_x = max((x for (x, y) in self.pixels))
            max_y = max((y for (x, y) in self.pixels))
        # Reconstruct all symbol values
        rows = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                try:
                    row.append(self.pixels[(x, y)])
                except KeyError:
                    row.append(self.default_pixel)
            rows.append(row)
        # Display
        output = '\n'.join((''.join((self.symbol_dict[j]) for j in row)
                            for row in rows))
        if clear:
            self.clear()
        print("\n{0}\n{1}\n".format(output, legend))

    def refresh(self, pixels, legend='', clear=True):
        self.update(pixels)
        self.show(legend=legend, clear=True)


class Graph():

    def __init__(self, nodes=[], edges={}):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, nodeA, nodeB, cost=1, two_ways=False):
        self.edges[(nodeA, nodeB)] = cost
        if two_ways:
            self.edges[(nodeB, nodeA)] = cost

    def remove_node(self, node):
        self.nodes.remove(node)
        edges = [x for x in self.edges if (x[0] == node or x[1] == node)]
        for edge in edges:
            del self.edges[edge]

    def a_star(self, start, goal, heuristic):
        """Runs the A* path searching algorithm

        Args:
            start (tuple):
                The starting nodecoordinates.
            goal (tuple):
                The objective node coordinates.
            heuristic (function):
                The heuristic cost as a function of node coordinates.
                The function shall support tuples as input.
        """
        def reconstruct_path(came_from, current):
            total_path = [current]
            while current in came_from:
                current = came_from[current]
                total_path.append(current)
            total_path.reverse()
            return total_path

        # The set of discovered nodes
        open_set = []
        heapq.heappush(open_set, (0, start))
        # Map of origins for the cheapest paths to each node
        came_from = {}
        # For node n, g_score(n) is the cheapest path cost from start to n
        g_score = {}
        g_score[start] = 0
        # Main loop
        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                return reconstruct_path(came_from, current)
            neighbours = [node for node in self.nodes
                          if (current, node) in self.edges]
            for neighbour in neighbours:
                tentative_g_score = \
                    g_score[current] + self.edges[(current, neighbour)]
                if tentative_g_score < g_score.get(neighbour, math.inf):
                    # This path to neighbour is better than any previous one
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    # For node n, f_score(n) = g_score(n) + heuristic(n)
                    f_score = g_score[neighbour] + heuristic(neighbour)
                    if neighbour not in open_set:
                        heapq.heappush(open_set, (f_score, neighbour))
        # Open set is empty but goal was never reached
        return None


def _find_sublist(mainlist, sublist, start=0):
    length = len(sublist)
    for index in range(start, len(mainlist)):
        if mainlist[index:index+length] == sublist:
            return index, index + length


def replace_sublist(mainlist, sublist, replacement):
    length = len(replacement)
    index = 0
    for start, end in iter(lambda: _find_sublist(mainlist, sublist, index),
                           None):
        mainlist[start:end] = replacement
        index = start + length


def split_list(mainlist, delmiter):
    outlist = []
    index = 0
    for start, end in iter(lambda: _find_sublist(mainlist, delmiter, index),
                           None):
        outlist.append(mainlist[index:start])
        index = end
    outlist.append(mainlist[index:])
    return outlist
