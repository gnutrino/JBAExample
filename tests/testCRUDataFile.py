#!/usr/bin/env python3

import unittest as ut
from datafile import CRUDataFile

class TestCRUDataFile(ut.TestCase):
    file_name = 'TestData'
    def setUp(self):
        self._file = open(self.file_name, 'r')

    def tearDown(self):
        self._file.close()

    def test_read_header(self):
        data = CRUDataFile(self._file)
        data.read_header()

        self.assertEqual(data.minYear, 1991)
        self.assertEqual(data.maxYear, 2000)
        self.assertEqual(data.extension, '.pre')
        self.assertEqual(data.parameter, 'precipitation')
        self.assertEqual(data.units, 'mm')
        self.assertEqual(data.numBoxes, 2)
