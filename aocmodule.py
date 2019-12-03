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

    def load(self, state, ip=0):
        self.memory = state
        self.ip = ip
        self.ishalted = False
        self.original = self.memory.copy()  # Save a static copy

    def load_from_file(self, file, ip=0):
        with open(file) as source:
            state = []
            for line in source:
                state = state + [int(item) for item in line.split(',')]
        self.load(state, ip)

    def rewind(self):
        # Reverts to last load
        self.load(self.original)

    def dsky(self, noun, verb):
        self.memory[1] = noun
        self.memory[2] = verb

    def step(self):
        # Fetch and execute next instruction
        opcode = self.memory[self.ip]
        if opcode == 1:
            # 3 parameters. MOV [IP+3], [IP+1] + [IP+2]
            self.memory[self.memory[self.ip+3]] = (
                self.memory[self.memory[self.ip+1]] +
                self.memory[self.memory[self.ip+2]])
            self.ip = self.ip + 4
        if opcode == 2:
            # 3 parameters. MOV [IP+3], [IP+1] * [IP+2]
            self.memory[self.memory[self.ip+3]] = (
                self.memory[self.memory[self.ip+1]] *
                self.memory[self.memory[self.ip+2]])
            self.ip = self.ip + 4
        if opcode == 99:
            # 1 parameters. NOP
            self.ishalted = True

    def execute(self):
        while not self.ishalted:
            self.step()
