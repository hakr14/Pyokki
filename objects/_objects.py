from typing import Union
from util import colors, parse_fraction

class PType:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color, self.light, self.dark = colors(color)
        self.eff: dict["PType", float] = {}

    def effectiveness(self, ptype: "PType", second_type: Union["PType", None] = None):
        if second_type is None:
            return self.eff[ptype]
        else:
            return self.effectiveness(ptype) * self.effectiveness(second_type)

    def __str__(self):
        return self.name

class Stat:
    def __init__(self, name: str, abbr: str, color: str, short: str = "", symbol: str = None, star: str = ""):
        self.name = name
        self.abbr = abbr
        self.color, self.light, self.dark = colors(color)
        if short == "":
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
                if mults[i] != "":
                    m = parse_fraction(mults[i])
            except IndexError:
                pass
            self.multipliers[keys[i]] = m