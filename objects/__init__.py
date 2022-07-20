from collections import OrderedDict
import objects._objects
from typing import Generic, TypeVar
from util import parse_fraction, parse_pyk

_VT = TypeVar("_VT")
class PDict(OrderedDict[str, _VT], Generic[_VT]):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
    
    def __getitem__(self, item: str):
        for k, v in self.items():
            if k == item:
                return v
        return self.nth(0)
    
    def nth(self, n: int) -> _VT:
        return list(self.values())[n]

TYPES: PDict[_objects.PType] = PDict()
for t in parse_pyk("pyk/type/ptypes.pyk"):
    TYPES[t[0]] = _objects.PType(*t)
l = len(TYPES)
c = parse_pyk("pyk/type/table.pyk")
for i in range(l):
    t = TYPES.nth(i)
    e = {}
    for j in range(l):
        e[TYPES.nth(j)] = parse_fraction(c[i][j])
    t.eff = e

STATS: PDict[_objects.Stat] = PDict()
s = parse_pyk("pyk/stats.pyk")
HEALTH = s[0][1]
STATS[s[0][1]] = _objects.Stat(*s[0])
for r in s[1:]:
    STATS[r[1]] = _objects.Stat(*r)

NATURES: PDict[_objects.Nature] = PDict()
f = parse_pyk("pyk/natures.pyk")
k = tuple(map(STATS.get, f[0][1:]))
for l in f[1:]:
    NATURES[l[0]] = _objects.Nature(*l, keys = k)

GENDERS: PDict[_objects.Gender] = PDict()
for g in parse_pyk("pyk/breeding/gender/genders.pyk"):
    GENDERS[g[0]] = _objects.Gender(*g)
l = len(GENDERS)
f = parse_pyk("pyk/breeding/gender/table.pyk")
for i in range(l):
    GENDERS.nth(i).compatibilities = {GENDERS.nth(j): bool(f[i][j]) for j in range(l)}

GROUPS: PDict[_objects.Group] = PDict()
for g in parse_pyk("pyk/breeding/group/groups.pyk"):
    GROUPS[g[0]] = _objects.Group(*g)
l = len(GROUPS)
f = parse_pyk("pyk/breeding/group/table.pyk")
for i in range(l):
    GROUPS.nth(i).compatibilities = {GROUPS.nth(j): bool(f[i][j]) for j in range(l)}

RATES: PDict[_objects.LevelingRate] = PDict()
_f: list[bool] = []
f = parse_pyk("pyk/levels.pyk")
for r in f[0]:
    RATES[r] = _objects.LevelingRate(r)
    _f.append(True)
for l in RATES.values():
    l.exp[1] = 0
for l in range(1, len(f)):
    for r in range(len(RATES)):
        if _f[r]:
            _f[r] = False
            try:
                _f[r] = bool(f[l][r])
                RATES.nth(r).exp[l + 1] = int(f[l][r])
            except IndexError:
                pass

CATEGORIES: PDict[_objects.MoveCategory] = PDict()
for c in parse_pyk("pyk/categories.pyk"):
    CATEGORIES[c[0]] = _objects.MoveCategory(*c)

MOVES: PDict[_objects.Move] = PDict()
for m in parse_pyk("pyk/moves.pyk"):
    MOVES[m[0]] = _objects.Move(*m)