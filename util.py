from csv import reader
from functools import reduce
from operator import truediv
from pygame.color import Color
from unicodedata import numeric

def parse_pyk(filename: str) -> tuple[tuple[str, ...]]:
    with open(filename, encoding = "UTF-8") as f:
        return tuple(tuple(e.strip() for e in row) for row in reader(f.readlines(), delimiter='|', escapechar='\\'))

def parse_fraction(frac: str):
    if len(frac) == 1:
        return numeric(frac)
    else:
        return reduce(truediv, map(int, frac.translate({8260: "/", 8543: "1/"}).split("/")))

def colors(t: tuple[str, ...]):
    return tuple(map(lambda c: tuple(Color("#" + c)), t))