import unittest as ut
import sqlalchemy
import datetime

from sqlalchemy.orm import mapper, clear_mappers, sessionmaker
from db import CRUTable

Session = sessionmaker()

class DummyRow():
    """dummy class for use in mapper to allow queries to run through the
    sqlalchemy ORM for testing the result of inserts"""
    def as_dict(self):
        """returns a dictionary of non-private (not begining with _)
        attributes"""
        return {
                key:value for key, value in self.__dict__.items()
                if not key.startswith('_') and not callable(value)
            }

class testCRUTable(ut.TestCase):

    rows = [
        {
            'Xref'  : 1,
            'Yref'  : 148,
            'Date'  : datetime.date(1991,1,1),
            'Value' : 3020,
        },
        {
            'Xref'  : 1,
            'Yref'  : 311,
            'Date'  : datetime.date(2000,12,1),
            'Value' : 450,
        }
    ]

    def setUp(self):
        self.table = CRUTable('test', 'sqlite://')
        Session.configure(bind=self.table.database)
        self.session = Session()
        mapper(DummyRow, self.table._table)

    def tearDown(self):
        clear_mappers()
        self.session.close()


    def test_add_row(self):
        self.table.add_row(self.rows[0])

        rows = self.session.query(DummyRow).all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].as_dict(), self.rows[0])

    def test_add_multiple_rows(self):
        self.table.add_row(self.rows[0])
        self.table.add_row(self.rows[1])

        rows = self.session.query(DummyRow).all()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].as_dict(), self.rows[0])
        self.assertEqual(rows[1].as_dict(), self.rows[1])

    def test_add_rows(self):
        self.table.add_rows(self.rows)

        rows = self.session.query(DummyRow).all()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].as_dict(), self.rows[0])
        self.assertEqual(rows[1].as_dict(), self.rows[1])
    
    def test_primary_key_constraint_violation(self):
        self.table.add_row(self.rows[0])
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.table.add_row(self.rows[0])

