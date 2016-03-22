import unittest as ut
import sqlalchemy
import datetime

from db import DataBase, CRUTable

class testDataBase(ut.TestCase):
    def setUp(self):
        self.db = DataBase('sqlite://')

    def test_add_table(self):

        table = CRUTable('test')
        self.db.add_table(table)
        metadata = sqlalchemy.MetaData()
        metadata.reflect(self.db.engine)
        self.assertIn('test', metadata.tables)

class testCRUTable(ut.TestCase):
    def setUp(self):
        self.db = DataBase('sqlite://')
        self.table = CRUTable('test', self.db)

    def testAddRow(self):
        self.table.add_row(1,148,datetime.date(1991,1,1), 3020)

        rows = self.db.session.query(self.table.Row).all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], self.table.Row(1, 148, datetime.date(1991,1,1), 3020))

    def test_add_multiple_rows(self):
        self.table.add_row(1,148, datetime.date(1991,1,1), 3020)
        self.table.add_row(1,311, datetime.date(2000,12,1), 450)

        rows = self.db.session.query(self.table.Row).all()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], self.table.Row(1, 148, datetime.date(1991,1,1), 3020))
        self.assertEqual(rows[1], self.table.Row(1, 311, datetime.date(2000,12,1), 450))

    
    def test_primary_key_constraint_violation(self):
        self.table.add_row(1,148, datetime.date(1991,1,1), 3019)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.table.add_row(1,148, datetime.date(1991,1,1), 3020)

