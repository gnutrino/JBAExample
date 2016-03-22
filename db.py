#!/usr/bin/env python3

from sqlalchemy import Table, Column, MetaData, create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.types import Integer, Date

class DataBase():
    
    def __init__(self, uri, echo=False):
        """initialise a database connection from a uri.
        
        If echo is set to True, generated SQL statements will be output to the
        python logging system for debugging purposes"""

        self.engine = create_engine(uri, echo=echo)
        self.session = sessionmaker(bind=self.engine)()
        self.tables = []

    def add_table(self, table):
        """Adds a Table to the database, outputs CREATE statement if table does
        not already exist in the database"""
        self.tables.append(table)
        table._table.create(self.engine, checkfirst=True)
        table.session = self.session

class CRUTable():
    """Represents a table for CRU data in a database. must be added to a
    DataBase using DataBase.add_table before adding or reading Rows"""

    def __init__(self, table_name, database = None):
        self._table = Table(table_name, MetaData(),
                Column('Xref', Integer, primary_key=True),
                Column('Yref', Integer, primary_key=True),
                Column('Date', Date, primary_key=True),
                Column('Value', Integer),
            )
        self.Row = self._get_row()
        mapper(self.Row, self._table)
        
        if database is not None:
            database.add_table(self)


    def add_row(self, *args):

        row = self.Row(*args)
        self.session.add(row)


    def add_rows(self, rows, batch=1024):
        """Adds multiple rows from an iterator, batched into lots"""
        for n, row in enumerate(rows, start=1):
            if n % batch == 0:
                self.session.commit()
            self.add_row(*row)

        self.session.commit()

    def _get_row(self):
        """Returns a new Row class - needed to create multiple CRUTables in
        one process (e.g for testing) due to mapper binding metadata to the class"""
        class Row():
            """Represents a row in a CRUTable"""

            def __init__(self, xref, yref, date, value):
                self.Xref  = xref
                self.Yref  = yref
                self.Date  = date
                self.value = value

            def __eq__(self, other):
                return all([
                    self.Xref  == other.Xref,
                    self.Yref  == other.Yref,
                    self.Date  == other.Date,
                    self.Value == other.Value,
                ])
        return Row
