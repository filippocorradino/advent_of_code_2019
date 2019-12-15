"""
Advent of Code 2019 - Utilities Module
https://adventofcode.com/2019/

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


class Intcode():

    def __init__(self, state=[]):
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
        self.memory = state
        self.ip = ip
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
        self.inputBuffer = []
        self.outputBuffer = []

    # I/O methods

    def dsky(self, noun, verb):
        """DSKY input

        Receives DSKY-like input, i.e. a NOUN and VERB statement.

        Args:
            noun (int):
                NOUN part of the statement, goes to memory[1].
            verb (int):
                VERB part of the statement, goes to memory[2].
        """
        self.memory[1] = noun
        self.memory[2] = verb

    def input(self, value):
        """General input

        Args:
            value (int):
                Numeric input to be pushed into the input buffer.
        """
        self.inputBuffer.append(value)

    def output(self):
        """General input

        Returns:
            output (int):
                Oldest item in the output buffer.
        """
        if self.outputBuffer:
            output = self.outputBuffer.pop(0)
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
        """
        modes = '{0:0{1}d}X'.format(raw_modes, n_parameters)
        modes = modes[::-1]
        values = [opcode]
        for offset in range(1, 1+n_parameters):
            parameter = self.memory[self.ip+offset]
            mode = modes[offset]
            if mode == '0':
                # Position mode
                values.append(self.memory[parameter])
            if mode == '1':
                # Immediate mode
                values.append(parameter)
        return modes, values

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
        opcode, raw_modes = self._parse_opcode(self.memory[self.ip])
        if opcode == 1:
            # 3 parameters. MOV [IP+3], (IP+1) + (IP+2)
            nParams = 3
            modes, values = self._parse_parameters(opcode, raw_modes, nParams)
            assert modes[3] == '0'  # Output always position mode
            self.memory[self.memory[self.ip+3]] = values[1] + values[2]
            self._std_ip_advance(nParams)
        if opcode == 2:
            # 3 parameters. MOV [IP+3], (IP+1) * (IP+2)
            nParams = 3
            modes, values = self._parse_parameters(opcode, raw_modes, nParams)
            assert modes[3] == '0'  # Output always position mode
            self.memory[self.memory[self.ip+3]] = values[1] * values[2]
            self._std_ip_advance(nParams)
        if opcode == 3:
            # 1 parameter. MOV [IP+1], IN
            nParams = 1
            modes, values = self._parse_parameters(opcode, raw_modes, nParams)
            assert modes[1] == '0'  # Save always position mode
            if self.inputBuffer:  # Input available
                self.iswaiting = False  # Clear waiting condition, if any
                self.memory[self.memory[self.ip+1]] = self.inputBuffer.pop(0)
                self._std_ip_advance(nParams)
            else:
                self.iswaiting = True
        if opcode == 4:
            # 1 parameter. MOV OUT, (IP+1)
            nParams = 1
            _, values = self._parse_parameters(opcode, raw_modes, nParams)
            self.outputBuffer.append(values[1])
            self._std_ip_advance(nParams)
        if opcode == 5:
            # 2 parameters. JNZ (IP+2)
            nParams = 2
            _, values = self._parse_parameters(opcode, raw_modes, nParams)
            if values[1] is not 0:
                self.ip = values[2]
            else:
                self._std_ip_advance(nParams)
        if opcode == 6:
            # 2 parameters. JEZ (IP+2)
            nParams = 2
            _, values = self._parse_parameters(opcode, raw_modes, nParams)
            if values[1] is 0:
                self.ip = values[2]
            else:
                self._std_ip_advance(nParams)
        if opcode == 7:
            # 3 parameters. MOV [IP+3], (IP+1) < (IP+2)
            nParams = 3
            modes, values = self._parse_parameters(opcode, raw_modes, nParams)
            assert modes[3] == '0'  # Output always position mode
            if values[1] < values[2]:
                result = 1
            else:
                result = 0
            self.memory[self.memory[self.ip+3]] = result
            self._std_ip_advance(nParams)
        if opcode == 8:
            # 3 parameters. MOV [IP+3], (IP+1) == (IP+2)
            nParams = 3
            modes, values = self._parse_parameters(opcode, raw_modes, nParams)
            assert modes[3] == '0'  # Output always position mode
            if values[1] == values[2]:
                result = 1
            else:
                result = 0
            self.memory[self.memory[self.ip+3]] = result
            self._std_ip_advance(nParams)
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
            self.nodes.update({tag: Intcode()})

    def add_ports(self, tags):
        """Add a set of ports (or make some node ports)

        Args:
            tags (Iterable):
                Tags to refer to the ports.
        """
        for tag in tags:
            if tag not in self.nodes:
                self.nodes.update({tag: Intcode()})
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
                raise KeyError("Target is not a valid node/port of the network")

    def step(self):
        """Programs step

        Executes one instruction cycle for each node in the network.
        Also pushes up to one item of data along each I/O pipe.
        Supports multiple pipes connected to a same node, in which case the
        outgoing value is copied over all the pipes.
        """
        for node in self.nodes:
            self.nodes[node].step()
            outPipes = [pipe for pipe in self.pipes if pipe[0] == node]
            if outPipes:
                item = self.nodes[node].output()
                if item is not None:
                    for pipe in outPipes:
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
