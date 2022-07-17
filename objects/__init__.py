import objects._objects
from util import *

TYPES: dict[str, _objects.PType] = {}
_types = []
for t in parse_pyk("pyk/type/ptypes.pyk"):
    name = t[0]
    TYPES[name] = _objects.PType(name, colors(t[1:]))
    _types.append(name)
n = len(_types)
c = parse_pyk("pyk/type/table.pyk")
for i in range(n):
    t = TYPES[_types[i]]
    e = {}
    for j in range(n):
        e[TYPES[_types[j]]] = parse_fraction(c[i][0][j])
    t.eff = e
del _types, t, name, n, c, i, e, j