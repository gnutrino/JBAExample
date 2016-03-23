#!/usr/bin/env python3

from datafile import CRUDataFile
from db import CRUTable
from argparse import ArgumentParser

def parse_args(argv):
    parser = ArgumentParser(description='Read data from file, transform and store in a database.')
    parser.add_argument(
            'fname', 
            metavar='FILE',
            help='File(s) to read data from'
        )
    parser.add_argument(
            '-t', '--table-name',
            help='Name of the database table to store data in. If not provided\
                  a table name will be computed from the header of FILE'
        )
    parser.add_argument(
            '-d', '--database',
            help="Specifies the database to use in SQLAlchemy URI form, default is 'sqlite:///FILE.db'"
        )
    parser.add_argument(
            '-b', '--batch',
            default=120000,
            type=int,
            help='Batch size for inserts into the database. Too low a value\
                  can cause performance issues, too high a value may cause\
                  database errors depending on the driver used. Defaults to\
                  120,000 (1000 grid boxes worth of data)'
        )
    parser.add_argument(
            '-a', '--append',
            action='store_true',
            help='Allows appending data to an existing table. If not set the\
                  table will be dropped and recreated if it already exists'
        )
    parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Causes generated SQL statements to be echoed to stderr for debugging purposes'
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

        table = CRUTable(args.table_name, args.database, append=args.append, echo=args.verbose)

        table.add_rows(datafile.data_points(), batch_size=args.batch)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
