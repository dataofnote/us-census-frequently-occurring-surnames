"""
Combines the 1990 and 2000 data surname data into one table
"""
from pathlib import Path
from csv import DictWriter, DictReader
import re

CORRAL_DIR = Path('wrangle', 'corral')
FETCHED_DIR = CORRAL_DIR / 'fetched'
SRC_PATHS = {'1990': FETCHED_DIR.joinpath('census-1990', 'surnames.txt'),
             '2000': FETCHED_DIR.joinpath('census-2000', 'app_c.csv')
            }

# This script sends it right to ./data
DEST_PATH = Path('data', 'us-census-surnames--1990-2000.csv')
DEST_PATH.parent.mkdir(exist_ok=True, parents=True)

RX_ROW_1990 = r'^(.+?)(?=\s*\d)(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)'
# The 1990 data looks like:
# SMITH          1.006  1.006      1
# JOHNSON        0.810  1.816      2
# WILLIAMS       0.699  2.515      3

def main():
    # We open the 2000 file first because it has the headers
    print("Reading from:", SRC_PATHS['2000'])
    csv2000 = DictReader(SRC_PATHS['2000'].read_text().splitlines())
    # awkward but whatever. We need to use csv2000's headers
    # and add the 'year' column to it
    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=['year'] + csv2000.fieldnames)
    destcsv.writeheader()
    for i, row in enumerate(csv2000):
        row['year'] = 2000
        destcsv.writerow(row)
    print("Wrote {0} lines to: {1}".format(i+1, DEST_PATH))

    # now we open 1990 file and iterate
    print("Reading from:", SRC_PATHS['1990'])
    for i, line in enumerate(SRC_PATHS['1990'].read_text().splitlines()):
        name, freq, cumfreq, rank = re.search(RX_ROW_1990, line).groups()
        row = { 'name': name.strip(),
                'rank': int(rank),
                'year': 1990,
                'prop100k': int(float(freq) * 1000),
                'cum_prop100k': int(float(cumfreq) * 1000),
              }
        destcsv.writerow(row)
    print("Wrote {0} lines to: {1}".format(i+1, DEST_PATH))
    # all done
    destfile.close()


if __name__ == '__main__':
    main()
