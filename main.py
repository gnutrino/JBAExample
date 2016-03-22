#!/usr/bin/env python3

from datafile import CRUDataFile
from db import DataBase, CRUTable
from argparse import ArgumentParser
from itertools import islice

def parse_args(argv):
    parser = ArgumentParser(description='Read data from file, transform and store in a database.')
    parser.add_argument(
            'fname', 
            metavar='FILE',
            help='File to read data from'
        )
    parser.add_argument(
            '-t', '--table-name',
            help='Name of database table to store values'
        )
    parser.add_argument(
            '-d', '--database',
            help="Specifies the database to use in SQLAlchemy URI form, default is 'sqlite:///FILE.db'"
        )
    parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            action='store_true',
            help='Causes generated SQL statements to be echoed to stderr for debugging purposes'
        )
    parser.add_argument(
            '-b', '--batch',
            type=int,
            default=1024,
            help='Number of datapoints written to the database per transaction.\
                  Too low a value will cause performance issues. Defaults to 1024'
        )

    args = parser.parse_args(argv)
    if not args.database:
        args.database = "sqlite:///{}.db".format(args.fname)

    return args

def get_default_table_name(datafile):
    datafile.read_header()
    default = datafile.info + ' ' + datafile.parameter
    default = default.lower()
    default = default.replace(' ', '_')
    return default

def main(argv):
    args = parse_args(argv)
    with open(args.fname, 'r') as f:
        datafile = CRUDataFile(f)
        if not args.table_name:
            args.table_name = get_default_table_name(datafile)

        database = DataBase(args.database, echo = args.verbose)
        table = CRUTable(args.table_name, database)

        table.add_rows(datafile.data_points(), batch=args.batch)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
