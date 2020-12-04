#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Tests

I'm still learning about testing in Python, and this is an unusual application
Apologies if this turns out to be ugly

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

import unittest


class TestResults(unittest.TestCase):

    solutions = {'day01_1': 3348909,
                 'day01_2': 5020494,
                 'day02_1': 2890696,
                 'day02_2': 8226,
                 'day03_1': 1285,
                 'day03_2': 14228,
                 'day04_1': 1063,
                 'day04_2': 686,
                 'day05_1': 13285749,
                 'day05_2': 5000972,
                 'day06_1': 261306,
                 'day06_2': 382,
                 'day07_1': 567045,
                 'day07_2': 39016654,
                 'day08_1': 1064,
                 'day08_2': ('   ██    ██  ███  ██ ██ █\n'
                             ' ██ █ ████ ██ █ ██ █ █ ██\n'
                             ' ██ █   ██ ████ ██ █  ███\n'
                             '   ██ ████ ████    █ █ ██\n'
                             ' ████ ████ ██ █ ██ █ █ ██\n'
                             ' ████ █████  ██ ██ █ ██ █'),
                 'day09_1': 3989758265,
                 'day09_2': 76791,
                 'day10_1': 253,
                 'day10_2': 815,
                 'day11_1': 2021,
                 'day11_2': ('█ ████   ████  █ ██ █    █ ██ █ ████ ██ ███\n'
                             '█ ████ ██ ████ █ ██ █ ████ █ ██ ████ ██ ███\n'
                             '█ ████   █████ █    █   ██  ███ ████    ███\n'
                             '█ ████ ██ ████ █ ██ █ ████ █ ██ ████ ██ ███\n'
                             '█ ████ ██ █ ██ █ ██ █ ████ █ ██ ████ ██ ███\n'
                             '█    █   ███  ██ ██ █    █ ██ █    █ ██ ███'),
                 'day12_1': 8625,
                 'day12_2': 332477126821644,
                 'day13_1': 247,
                 'day13_2': 12954,
                 'day14_1': 1582325,
                 'day14_2': 2267486,
                 'day15_1': 236,
                 'day15_2': 368,
                 'day16_1': 19944447,
                 'day16_2': 81207421,
                 'day17_1': 2804,
                 'day17_2': 833429}

    def test_results(self):
        """
        Test all challenges scripts results
        """
        for script in self.solutions:
            print("Testing {0}.py...".format(script))
            with self.subTest(i=script):
                module = __import__(script)
                self.assertEqual(module.main(), self.solutions[script])
        print("All done")


if __name__ == '__main__':
    unittest.main()
