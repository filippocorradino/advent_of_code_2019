#!/usr/bin/env python
# encoding: utf-8
"""
Advent of Code 2019 - Day 14 - Challenge 1
https://adventofcode.com/2019/day/14

Solution: 1582325

PEP 8 compliant
"""

__author__ = "Filippo Corradino"
__email__ = "filippo.corradino@gmail.com"

import re
from math import ceil


def parse_recipes(filename):
    recipes = {}
    regex = r'(\d+)\s([A-Z]+)'
    with open(filename, 'r') as file:
        for line in file:
            items = re.findall(regex, line)
            # Output: list of (QTY, REAGENT) tuples. Last one is the product.
            product = items[-1][-1]
            recipes.update(
                {product: {reagent: int(qty) for (qty, reagent) in items}})
    return recipes


def rank_products(recipes, target):
    rank = 0
    ranks = {target: rank}
    while True:
        rank = rank + 1
        products = [product for product in ranks
                    if ranks[product] == (rank - 1) and product in recipes]
        if not products:
            break  # Reached bottom level, no updates
        for product in products:
            ranks.update({reagent: rank for reagent in recipes[product]
                         if reagent != product})
    return ranks


def basecost_product(recipes, target, qty=1):
    ranks = rank_products(recipes, target)
    rank = 0
    costs = {product: 0 for product in ranks}
    costs[target] = qty
    while True:
        products = [product for product in ranks
                    if ranks[product] == rank and product in recipes]
        if not products:
            break  # Reached bottom level, no updates
        for product in products:
            req_qty = costs[product]
            min_qty = recipes[product][product]
            n_cycles = ceil(req_qty / min_qty)
            for reagent in recipes[product]:
                if reagent != product:
                    costs[reagent] = \
                        costs[reagent] + n_cycles * recipes[product][reagent]
            costs[product] = 0
        rank = rank + 1
    return costs


def main(target='FUEL', source='ORE', n_target=1, printout=False):
    recipes = parse_recipes('inputs/day_14_input.txt')
    costs = basecost_product(recipes, target, n_target)
    n_source = costs[source]
    if printout:
        print("\nNumber of necessary {0} for 1 {1}: {2}\n"
              .format(source, target, n_source))
    return n_source


if __name__ == "__main__":
    main(printout=True)
