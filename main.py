#!/usr/bin/env python3

from datafile import CRUDataFile
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description='Read data from file, transform and store in a database.')
    parser.add_argument(
            'fname', 
            metavar='FILE',
            help='File to read data from'
        )
    parser.add_argument(
            '-t', '--table-name',
            nargs='?',
            help='Name of database table to store values'
        )

    args = parser.parse_args()

    with open(args.fname, 'r') as f:
        data = CRUDataFile(f)
        data.read_header()
        print(data.__dict__)

