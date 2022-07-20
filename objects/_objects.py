from functools import reduce
from operator import mul
from util import colors, parse_fraction

class _NameColor:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color, self.light, self.dark = colors(color)
    
    def __str__(self):
        return self.name

class PType(_NameColor):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)
        self.eff: dict["PType", float] = {}

    def effectiveness(self, *ptypes: "PType"):
        return reduce(mul, map(self.eff.get, ptypes))

class Stat(_NameColor):
    def __init__(self, name: str, abbr: str, color: str, short: str = None, symbol: str = None, star: str = None):
        super().__init__(name, color)
        self.abbr = abbr
        if short is None:
            self.short_name = name
        else:
            self.short_name = short
        self.symbol = symbol
        self.display = not bool(star)

    def __str__(self):
        return self.abbr

    def __repr__(self):
        return f"Stat({self.name}, {self.abbr}, {self.color}, {self.short_name}, {self.symbol}, {self.display})"

class Nature:
    def __init__(self, name: str, *mults: str, keys: tuple[Stat, ...]):
        self.name = name
        self.multipliers: dict[Stat, float] = {}
        for i in range(len(keys)):
            m = 1
            try:
                if mults[i] is not None:
                    m = parse_fraction(mults[i])
            except IndexError:
                pass
            self.multipliers[keys[i]] = m

class Gender(_NameColor):
    def __init__(self, name: str, color: str, pri: str, only: str = None):
        super().__init__(name, color)
        self.priority = int(pri)
        self.only = bool(only)
        self.compatibilities: dict["Gender", bool] = {}
    
    def compatible(self, gender: "Gender"):
        return self.compatibilities[gender]

class Group(_NameColor):
    def __init__(self, name: str, color: str, only: str = None):
        super().__init__(name, color)
        self.only = bool(only)
        self.compatibilities: dict["Group", bool] = {}
    
    def compatible(self, *groups: "Group"):
        return any(map(self.compatibilities.get, groups))

class LevelingRate:
    def __init__(self, name: str):
        self.name = name
        self.exp: dict[int, int] = {}
    
    def level_at(self, exp: int):
        level = 1
        for l, e in self.exp.items():
            if e > exp:
                break
            level = l
        return level
    
    def exp_to_next(self, curr_exp: int):
        try:
            return self.exp[self.level_at(curr_exp) + 1] - curr_exp
        except IndexError:
            return 0
    
    def __str__(self):
        return self.name
    
    def __getitem__(self, item: int):
        return self.exp[item]

class MoveCategory(_NameColor):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)

class Move:
    def __init__(self, name: str, ptype: str, category: str, pp: str, power: str, acc: str, target: str, wide: str = None, flags: str = None, additional: str = None):
        from objects import CATEGORIES, TYPES
        self.name = name
        self.type = TYPES[ptype]
        self.category = CATEGORIES[category]
        self.pp = int(pp)
        self.power = int(power)
        self.accuracy = int(acc) / 100
        self.target = tuple(bool(int(target) >> i & 1) for i in range(5, -1, -1))
        self.wide = bool(wide)
        self.flags = list(flags or "")
        self.additional = additional or ""
    
    def do_additional(self, *args):
        ...
    
    def __str__(self):
        return self.name
    
    def __getitem__(self, item: str):
        return item in self.flags