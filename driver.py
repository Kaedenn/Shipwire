#!/usr/bin/env python

# driver.py
import orders
import inventory
import allocator

import argparse
import logging
import sys

"""
p = argparse.ArgumentParser(usage="%(prog)s <radius> [args...]",
                                epilog=METHOD_DESCRIPTION)
    p.add_argument("radius", type=float)
    p.add_argument("--width", type=int, default=0, metavar='W')
    p.add_argument("--height", type=int, default=0, metavar='H')
    p.add_argument("--method", choices=[METHOD_SIMPLE, METHOD_COMPLEX],
                   default=METHOD_SIMPLE)
    args = p.parse_args()
    r, w, h = args.radius, args.width, args.height
"""

def parseOrders(stream):
    return [json.loads(line.strip() for line in stream)]

def parseInventory(stream):
    "Expects either A=100,B=200,... or A=100\nB=200\n... formats"
    data = stream.read().strip().replace('\n', ',')
    logging.debug("Parsing inventory %s", repr(data))
    return list(i.split('=') for i in data.split(','))

if __name__ == "__main__":
    p = argparse.ArgumentParser(usage="%(prog)s [options...]", epilog = """
    If omitted, --orders defaults to "./orders.txt" and --inventory defaults
    to "./inventory.txt" """)
    p.add_argument("--orders", action="append", default=["orders.txt"], metavar="FILE")
    p.add_argument("--inventory", default="inventory.txt", metavar="FILE")
    p.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
    p.add_argument("-d", "--debug", action="store_true", help="debug mode")
    args = p.parse_args()

    if args.debug:
        logging.basicConfig(level = logging.DEBUG)

    if args.verbose:
        logging.basicConfig(level = logging.INFO)

    logging.debug("Beginning data allocation")
    logging.info("Loading inventory from %s", args.inventory)
    inv = inventory.Inventory.FromString(open(args.inventory).read())

    allocator = allocator.Allocator(inv)
    for orderSource in args.orders:
        logging.info("Loading order source from %s", orderSource)
        allocator.addOrderSource(orders.OrderFile(orderSource))

    logging.debug("Finished data allocation, allocating orders...")
    for allocation in allocator.allocate():
        print allocation.order(), inventory.Inventory.AmountsToString(allocation.allocation())
    logging.debug("Finished allocating orders")
