#!/usr/bin/env python3

from itertools import islice

from sqlalchemy import Table, Column, MetaData, create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.types import Integer, Date

def chunk(iterator, batch_size):
    """utility function to batch an iterable into chunks without reading it all
    into memory"""
    iterator = iter(iterator)
    while True:
        chunk = tuple(islice(iterator, batch_size))
        if not chunk:
            return
        yield chunk

class CRUTable():
    """Represents a table for CRU data in a database."""

    def __init__(self, table_name, database_uri, echo=False):
        self._table = Table(table_name, MetaData(),
                Column('Xref', Integer, primary_key=True),
                Column('Yref', Integer, primary_key=True),
                Column('Date', Date, primary_key=True),
                Column('Value', Integer),
            )
        self.database = create_engine(database_uri, echo=echo)
        self.create()

    def create(self, checkfirst=True):
        """Creates the table in the database. If checkfirst is True will not
        attempt to create an already existing table"""
        self._table.create(self.database, checkfirst=checkfirst)
        
    def add_row(self, row):
        """Adds a row to the table. 
        row should be a dict of the form { column_name: value, ... }"""
        self.database.execute(self._table.insert(row))

    def add_rows(self, rows, batch_size=120000):
        """Adds multiple rows from an iterator."""
        for batch in chunk(rows, batch_size):
            self.database.execute(
                    self._table.insert(),
                    batch
            )
