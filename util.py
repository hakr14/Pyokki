from csv import reader

def parse_pyk(filename: str):
    return reader(filename, delimiter='|', escapechar='\\')