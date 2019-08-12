#
# Data relating to a single company.
#

class Company(object):
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
