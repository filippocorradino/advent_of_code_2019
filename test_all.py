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

    solutions = {'day1_1': 3348909,
                 'day1_2': 5020494,
                 'day2_1': 2890696,
                 'day2_2': 8226,
                 'day3_1': 1285,
                 'day3_2': 14228,
                 'day4_1': 1063,
                 'day4_2': 686,
                 'day5_1': 13285749,
                 'day5_2': 5000972,
                 'day6_1': 261306,
                 'day6_2': 382,
                 'day7_1': 567045,
                 'day7_2': 39016654,
                 'day8_1': 1064,
                 'day8_2': ('1110011110011000110010010'
                            '1001010000100101001010100'
                            '1001011100100001001011000'
                            '1110010000100001111010100'
                            '1000010000100101001010100'
                            '1000010000011001001010010'),
                 'day9_1': 3989758265,
                 'day9_2': 76791}

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
