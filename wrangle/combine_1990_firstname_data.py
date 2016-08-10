"""
Combines the male and female firstnames data file
"""
from pathlib import Path
import csv
import re

SRC_DIR = Path('data', 'fetched', 'census-1990')
DEST_PATH = Path('data', 'compiled', 'us-census-1990-firstnames.txt')
DEST_PATH.parent.mkdir(exist_ok=True, parents=True)

HEADERS = ['year', 'name', 'gender', 'rank_within_gender', 'frequency', 'cumulative_frequency']
THE_YEAR = 1990

RX_ROW_1990 = r'^(.+?)(?=\s*\d)(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)'
# The 1990 data looks like:
# MARY           2.629  2.629      1
# PATRICIA       1.073  3.702      2

def main():
    destfile = DEST_PATH.open('w')
    destcsv = csv.writer(destfile)
    destcsv.writerow(HEADERS)

    for gender in ('female', 'male'):
        src_path = SRC_DIR / ('firstnames-%s.txt' % gender)
        print("Reading from:", src_path)
        for i, line in enumerate(src_path.open()):
            name, freq, cumfreq, rank = re.search(RX_ROW_1990, line).groups()
            destcsv.writerow([THE_YEAR, name.strip(), gender, rank, freq, cumfreq])
        print("Wrote {0} lines to: {1}".format(i+1, DEST_PATH))
    destfile.close()


if __name__ == '__main__':
    main()
