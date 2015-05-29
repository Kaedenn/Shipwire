#!/usr/bin/env python

# inventory.py

import logging

class Inventory(object):
    @classmethod
    def FromString(self, string):
        data = string.strip().replace('\n', ',')
        return Inventory(list(i.split('=') for i in data.split(',')))

    def ToString(self):
        return self.AmountsToString(self._inventory)

    @classmethod
    def AmountsToString(self, inventory):
        return ','.join("%s=%s" % (k,inventory[k]) for k in sorted(inventory))

    def __init__(self, source):
        """Initialize the inventory with the data provided in `source'. The
        parameter must be a tuple of (item-name, item-amount)"""
        logging.debug("Loading data %s", source)
        self._inventory = dict((k,int(v)) for k,v in source)

    def getInventory(self, item):
        """Returns how much of `item' is in stock. Raises an error on invalid
        items"""
        return self._inventory[item]

    def getAllInventory(self):
        "Returns a tuple of (item-name, item-amount) for all items"
        return tuple((na,am) for na,am in self._inventory.items())

    def order(self, item, amount):
        """Returns a pair of (item-name, ordered-amount) and decreases the
        internal count of items by at most the amount specified. The returned
        ordered-amount may be less than `amount' if not enough of that item
        exists in stock"""
        actual = min(amount, self._inventory[item])
        self._inventory[item] -= actual
        logging.debug("Satisfied %s of %s on %s", actual, amount, item)
        logging.info(self.ToString())
        return item, actual

