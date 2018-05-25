from collections import OrderedDict


class Symbol(object):
    def __init__(self, name, stype=None):
        self.name = name
        self.stype = stype

    def __repr__(self):
        return '<{}:{}>'.format(self.name, self.stype)

class PrimitiveSymbol(Symbol):
    pass


class VariableSymbol(Symbol):
    pass


class SymbolTable(object):
    def __init__(self):
        self._symbols = OrderedDict()

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self._symbols.values()]
        )
        return s

    __repr__ = __str__

    def define(self, name, value):
        self._symbols[name] = value

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        return symbol
