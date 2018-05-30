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
        self.scopes = [OrderedDict()]

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self.scopes[-1].values()]
        )
        return s

    __repr__ = __str__

    def define(self, name, value):
        self.scopes[-1][name] = value

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self.scopes[-1].get(name)
        return symbol

    def push_scope(self):
        self.scopes.append(OrderedDict(self.scopes[-1]))

    def pop_scope(self):
        if len(self.scopes) == 1:
            return False
        return self.scopes.pop()

