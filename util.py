from csv import reader
from functools import reduce
from operator import truediv
from pygame.color import Color
from unicodedata import numeric

def parse_pyk(filename: str) -> tuple[tuple[str | None, ...], ...]:
    with open(filename, encoding = "UTF-8") as f:
        return tuple(filter(lambda v: v is not None, (tuple(e.strip() or None for e in row) if len(row) > 1 else tuple(e.strip() for e in row[0]) if len(row) == 1 else None for row in reader(f.readlines(), delimiter='|', escapechar='\\'))))

def parse_fraction(frac: str):
    if len(frac) == 1:
        return numeric(frac)
    else:
        return reduce(truediv, map(int, frac.translate({8260: "/", 8543: "1/"}).split("/")))

def colors(col: str):
    c = Color("#" + col)
    l = Color(int(c.r + (255 - c.r) * 0.35), int(c.g + (255 - c.g) * 0.35), int(c.b + (255 - c.b) * 0.35))
    d = Color(int(c.r * 0.65), int(c.g * 0.65), int(c.b * 0.65))
    return tuple(c), tuple(l), tuple(d)