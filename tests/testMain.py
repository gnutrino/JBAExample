import unittest as ut
import os
import main
import sqlite3

def rel_path(path):
    """utility function to make path relative to __file__ directory"""
    return os.path.join(os.path.dirname(__file__), path)

class testFuncs(ut.TestCase):
    def test_get_default_table_name(self):
        from datafile import CRUDataFile
        datafile = CRUDataFile(open(os.path.join(os.path.dirname(__file__), 'TestData'), 'r'))
        name = main.get_default_table_name(datafile)
        self.assertEqual(name, 'tyndall_centre_grim_precipitation')

    def test_parse_args_defaults(self):
        argv = ['TestData']
        args = main.parse_args(argv)

        self.assertEqual(args.fname, 'TestData')
        self.assertIsNone(args.table_name)
        self.assertEqual(args.database, 'sqlite:///TestData.db')
        self.assertEqual(args.batch, 120000)
        self.assertFalse(args.verbose)

    def test_parse_args_options(self):
        argv = ['-t', 'test_table', '-d', 'sqlite://', '-b', '120', '-v', 'TestData']
        args = main.parse_args(argv)

        self.assertEqual(args.fname, 'TestData')
        self.assertEqual(args.table_name, 'test_table')
        self.assertEqual(args.database, 'sqlite://')
        self.assertEqual(args.batch, 120)
        self.assertTrue(args.verbose)

class testMain(ut.TestCase):

    def setUp(self):
        self.datafile = rel_path('TestData')
        self.database = self.datafile + '.db'
        self.argv = ['-t', 'test_table', self.datafile]

    def tearDown(self):
        try:
            os.remove(self.database)
        except OSError:
            pass


    def test_main(self):
        main.main(self.argv)

        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        self.assertIn('test_table', (x for x, in cur.fetchall()))

        cur.execute("SELECT COUNT(*) FROM test_table")
        count, = cur.fetchone()
        self.assertEqual(count, 240)

