#!/usr/bin/env python

"""
datagen.py: Generates orders.txt based on supplied inventory
"""

import argparse
import json
import random

PRODUCTS = {
    "A": 150,
    "B": 150,
    "C": 100,
    "D": 100,
    "E": 200
}

def addProduct(products, name, amount):
    assert name in products, "Unknown invalid item %s" % (name,)
    assert amount >= 0, "Amount %d for product %s must be positive" % (amount, name)
    products[name] = amount

class Order(object):
    OrderStr = "{'Header': %s, 'List': [%s]}"
    ItemStr = "{'Product': '%s', 'Quantity': %s}"
    def __init__(self, header):
        self._data = {"Header": header, "List": []}

    def addItem(self, product, quantity):
        self._data["List"].append({"Product": product, "Quantity": quantity})

    def __str__(self):
        return json.dumps(self._data)

if __name__ == "__main__":
    p = argparse.ArgumentParser(usage="$(prog)s [options...]", epilog = """
The layout of ORDERS must be of the form "str=num,str=num,..."
where each `str' is an item name (A..E) and `num' is a nonnegative integer.
For example, "A=150,B=150,C=100,D=100,E=200" is the default set. Passing
--inventorystr modifies inventory.txt. Omitting it and passing --inventory
reads inventory.txt. Omitting both ignores inventory.txt and uses the default
set. The program this supplies (parent directory) accepts both
"str=num,str=num,..." and "str=num\\nstr=num\\n..." formats for inventory.txt.
    """)
    p.add_argument("--orders", default="orders.txt", metavar="FILE",
                   help="write this file (default orders.txt)")
    p.add_argument("--inventorystr", default="", metavar="ORDERS",
                   help="write ORDERS (see below) to inventory.txt (or "
                   "whatever the value of --inventory is)")
    p.add_argument("--inventory", default="", metavar="FILE",
                   help="use this instead of inventory.txt")
    args = p.parse_args()

    if len(args.inventorystr) > 0:
        # read arg, write file
        items = args.inventorystr.split(',')
        for item in items:
            na, am = item.split('=')
            addProduct(PRODUCTS, na, int(am))
        # ew
        inventoryStream = open(args.inventory if args.inventory else "inventory.txt", 'w')
        for item in sorted(PRODUCTS):
            inventoryStream.write("%s=%d\n" % (item, PRODUCTS[item]))
    elif len(args.inventory) > 0:
        # read file
        inventoryStream = open(args.inventory)
        for line in inventoryStream:
            item, amount = line.strip().split('=')
            addProduct(PRODUCTS, item, int(amount))
    else:
        PRODUCTS['A'] = 150
        PRODUCTS['B'] = 150
        PRODUCTS['C'] = 100
        PRODUCTS['D'] = 100
        PRODUCTS['E'] = 200

    for product in sorted(PRODUCTS):
        print "Item '%s', amount '%d'" % (product, PRODUCTS[product])

    print "Generating orders..."

    orderStream = open(args.orders, 'w')
    header = 1
    while sum(PRODUCTS.values()) > 0:
        order = Order(header)
        header += 1
        # About half of the orders will have two requests; others will have one.
        for _ in xrange(random.choice((1, 2))):
            product = random.choice(PRODUCTS.keys())
            amount = random.randrange(1, 6)
            PRODUCTS[product] = max(PRODUCTS[product] - amount, 0)
            order.addItem(product, amount)
        orderStream.write("%s\n" % (order,))

    print "Generated %s orders" % (header,)

