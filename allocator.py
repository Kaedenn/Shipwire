#!/usr/bin/env python

# allocator.py

import logging

class Allocation(object):
    """Valid order-to-inventory allocation representation

    Represents how much of an order could be satisfied given the inventory
    available at the time of processing."""
    def __init__(self, order, allocation):
        self._order = order
        self._allocation = allocation

    def order(self):
        return self._order

    def allocation(self):
        return self._allocation

    def __str__(self):
        return "%s %s" % (self._order, self._allocation)

class Allocator(object):
    """Order-to-inventory allocation management object

    Basically, first-come-first-serve. When adding an order with
    addOrderSource, the source will only be examined after all current orders
    are satisfied/exhausted."""
    def __init__(self, inventory):
        self._inventory = inventory
        self._activeOrders = []
        self._orderSources = []

    def addOrderSource(self, source):
        """Add a batch of orders to the queue. The `source' parameter must be
        an iterable of Order objects.

        The batch will be processed only when all existing orders have been
        processed."""
        logging.debug("Adding order source %s", source.getStreamName())
        self._orderSources.append(source)
        self._activeOrders.append(iter(source))

    def nextOrder(self):
        """Shift the next order off of the queue

        * If there are no active batches of orders, return nothing.
        * Otherwise, shift the next order off of the next batch of orders and
          return that order.
        * If that batch is empty, remove it from the queue and proceed to the
          next batch of orders."""
        if not self._activeOrders:
            logging.debug("No active orders left")
            return None
        try:
            return next(self._activeOrders[0])
        except StopIteration, _:
            # batch has been exhausted
            logging.debug("Exhausted sequence, proceeding to next one")
            self._orderSources = self._orderSources[1:]
            self._activeOrders = self._activeOrders[1:]
            return self.nextOrder()

    def allocateOne(self):
        order = self.nextOrder()
        if order is None:
            return None
        logging.debug("Processing order %s", repr(order))
        satisfied = {}
        for item in order.items():
            name, count = item
            orderedName, orderedCount = self._inventory.order(name, count)
            satisfied[name] = orderedCount
            logging.debug("Satisfied %s of %s on item %s", satisfied[name],
                          count, name)
        return Allocation(order, satisfied)

    def allocate(self):
        order = self.allocateOne()
        while order is not None:
            yield order
            order = self.allocateOne()

