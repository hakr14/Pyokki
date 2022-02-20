import csv

def parse_pyk(filename):
    return csv.reader(filename, delimiter='|', escapechar='\\')