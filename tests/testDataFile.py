#!/usr/bin/env python3

import unittest as ut
import datetime
import os

from datafile import CRUDataFile, GridBox
from collections import namedtuple
from unittest.mock import sentinel

class TestCRUDataFile(ut.TestCase):

    file_name = os.path.join(os.path.dirname(__file__), 'TestData')
    #convenience for defining expected data values
    Data = namedtuple('Data', ['year', 'month', 'value'])
    expected_data1 = [
            Data(1991, 1, 3020),
            Data(1991, 2, 2820),
            Data(1992, 1, 3020),
            Data(1993, 4, 12880),
            Data(2000, 12, 2630),
        ]

    expected_data2 = [
            Data(1991, 1, 490),
            Data(1991, 2, 290),
            Data(1992, 1, 490),
            Data(1993, 4, 230),
            Data(2000, 12, 450),
        ]

    def setUp(self):
        self._file = CRUDataFile(open(self.file_name, 'r'))

    def tearDown(self):
        self._file._file.close()

    def test_read_header(self):
        datafile = self._file

        with self.assertRaises(ValueError):
            datafile.numYears

        datafile.read_header()

        self.assertEqual(datafile.minYear, 1991)
        self.assertEqual(datafile.maxYear, 2000)
        self.assertEqual(datafile.extension, '.pre')
        self.assertEqual(datafile.parameter, 'precipitation')
        self.assertEqual(datafile.units, 'mm')
        self.assertEqual(datafile.numBoxes, 2)
        self.assertEqual(datafile.numYears, 10)

    def check_data(self, data, expected):
        for d in expected:
            with self.subTest(d=d):
                index = 12*(d.year - 1991) + d.month - 1
                self.assertEqual(data[index], (datetime.date(d.year, d.month, 1), d.value))


    def test_read_gridbox(self):
        datafile = self._file

        datafile.read_header()

        grid = datafile.read_gridbox()

        self.assertIs(grid.xref, 1)
        self.assertIs(grid.yref, 148)

        self.check_data(grid.data, self.expected_data1)

        self.assertEqual(len(grid.data), 12*datafile.numYears)


    def test_gridboxes(self):
        datafile = self._file

        grids = list(datafile.gridboxes())

        self.assertEqual(grids[0].xref, 1)
        self.assertEqual(grids[0].yref, 148)

        self.check_data(grids[0].data, self.expected_data1)

        self.assertEqual(len(grids[0].data), 12*datafile.numYears)

        self.assertEqual(grids[1].xref, 1)
        self.assertEqual(grids[1].yref, 311)


        self.check_data(grids[0].data, self.expected_data1)

        self.assertEqual(len(grids[0].data), 12*datafile.numYears)

    def test_data_points(self):
        datafile = self._file

        data = list(datafile.data_points())

        self.assertEqual(data[0], {
            'Xref' : 1,
            'Yref' : 148,
            'Date' : datetime.date(1991,1,1),
            'Value': 3020,
        })

        self.assertEqual(data[-1], {
            'Xref' : 1,
            'Yref' : 311,
            'Date' : datetime.date(2000,12,1),
            'Value': 450,
        })

        self.assertEqual(len(data), datafile.numBoxes*datafile.numYears*12)
