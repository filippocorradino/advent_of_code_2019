#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 8 - Challenge 1
https://adventofcode.com/2019/day/8

Solution: 1064

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"


def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


def get_picture_layers(input_path, width, height):
    with open(input_path) as file:
        raw_picture = ''.join(line for line in file)
    return chunk_string(raw_picture, width*height)


def main():
    layers = list(get_picture_layers('inputs/day_08_input.txt', 25, 6))
    layer_metric = [layer.count('0') for layer in layers]
    min_layer = layer_metric.index(min(layer_metric))
    count1 = layers[min_layer].count('1')
    count2 = layers[min_layer].count('2')
    total_count = count1*count2
    print("\nNumber of 1 digits times number of 2 digits: {0}\n"
          .format(total_count))
    return total_count


if __name__ == "__main__":
    main()
