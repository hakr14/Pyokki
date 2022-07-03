from csv import reader
from typing import Iterable

def parse_pyk(filename: Iterable[str]):
    return reader(filename, delimiter='|', escapechar='\\')