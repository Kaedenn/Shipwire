#!/usr/bin/env python

# orders.py

import json

class Order(object):
    "Single-order object"
    def __init__(self, source, header, *items):
        self._source = source
        self._header = header
        self._items = []
        for item in items:
            self._items.append(tuple(item))

    def addItem(self, item, amount):
        self._items.append((item, amount))

    def header(self):
        return self._header
    def source(self):
        return self._source
    def items(self):
        for item in self._items:
            yield item[0], item[1]

    def __str__(self):
        result = '%s:%s ' % (self._source, self._header)
        result += ','.join("%s=%s" % item for item in sorted(self._items))
        return result

    def __repr__(self):
        return "Order('%s', '%s', *%s)" % (self._source, self._header, self._items)

class OrderFile(object):
    """Orders management object

    Orders must be valid JSON of the form
    {'Header': 282, 'List': [{'Product': 'A', 'Quantity': 4}]}
    where 'List' is a list of one or more items and 'Header' is a unique
    integer per request
    """
    def __init__(self, source):
        self._label = source
        self._stream = open(source)
        self._orders = []
        for line in self._stream:
            self._orders.append(self._orderFromJSON(line.strip()))

    def _orderFromJSON(self, line):
        order = json.loads(line)
        header = order['Header']
        items = []
        for item in order['List']:
            items.append((item['Product'], item['Quantity']))
        return Order(self._label, header, *items)

    def getStreamName(self):
        return self._label

    def __iter__(self):
        return iter(self._orders)


