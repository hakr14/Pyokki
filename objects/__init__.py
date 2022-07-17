import objects._objects
from util import parse_fraction, parse_pyk

TYPES: dict[str, _objects.PType] = {}
_types = []
for t in parse_pyk("pyk/type/ptypes.pyk"):
    n = t[0]
    TYPES[n] = _objects.PType(*t)
    _types.append(n)
l = len(_types)
c = parse_pyk("pyk/type/table.pyk")
for i in range(l):
    t = TYPES[_types[i]]
    e = {}
    for j in range(l):
        e[TYPES[_types[j]]] = parse_fraction(c[i][0][j])
    t.eff = e

STATS: dict[str, _objects.Stat] = {}
s = parse_pyk("pyk/stats.pyk")
HEALTH = s[0][1]
STATS[s[0][1]] = _objects.Stat(*s[0])
for r in s[1:]:
    STATS[r[1]] = _objects.Stat(*r)

NATURES: dict[str, _objects.Nature] = {}
f = parse_pyk("pyk/natures.pyk")
k = tuple(map(STATS.get, f[0][1:]))
for l in f[1:]:
    NATURES[l[0]] = _objects.Nature(*l, keys = k)