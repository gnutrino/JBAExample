from itertools import islice
from parse import parse
from collections import namedtuple
import datetime

class ParseException(Exception):
    pass

class CRUDataFile():
    """Represents a data file from the CRU TS 2.1 data set"""

    def __init__(self, file):
        self._file = file
        self._header_read = False

    def read_header(self):
        """reads the header from the file and populates minYear, maxYear,
        numBoxes, extension, parameter and units"""
        if self._header_read:
            return

        #The header consists of the first 5 lines of the file
        header = islice(self._file, 5)

        #formats to be accepted by parse for each header line
        header_formats = [
                "{info} file created on {} at {} by {}",
                "{extension} = {parameter} ({units})",
                "CRU TS 2.1",
                "[Long={}] [Lati={}] [Grid X,Y={}]",
                "[Boxes={numBoxes:>d}] [Years={minYear:d}-{maxYear:d}] [Multi={}] [Missing={}]",
            ]

        for line_num, result in enumerate(map(parse, header_formats, header)):
            if not result:
                raise ParseException("Error parsing header line {}".format(line_num))
            #named captures are added as attributes to self
            self.__dict__.update(result.named)

        #make sure we only run read_header once per file
        self._header_read = True

    def data_points(self):
        """Returns an iterator of datapoints in the file as dictionaries"""

        for grid in self.gridboxes():
            for date, value in grid.data:
                yield {
                    'Xref' : grid.xref,
                    'Yref' : grid.yref,
                    'Date' : date,
                    'Value': value
                    }

    @property
    def numYears(self):
        """Gets the number of years the data set encompases"""
        if not self._header_read:
            raise ValueError("numYears has no value until read_header() is called")
        return self.maxYear - self.minYear + 1

    def gridboxes(self):
        """Returns a generator of GridBoxes from the current file"""

        #make sure header is read
        self.read_header()

        while True:
            grid = self.read_gridbox()
            if grid is None:
                return
            yield grid

    def read_gridbox(self):
        """Returns a GridBox read from the current file read position or None is at EOF"""
        line = self._file.readline()
        if not line:
            return None

        grid_header = parse("Grid-ref={xref:>d},{yref:>d}", line)
        if not grid_header:
            raise ParseException("Invalid grid header: {}".format(line))

        grid = GridBox(**grid_header.named)

        for year in range(self.minYear, self.maxYear + 1):
            line = self._file.readline()
            for month, value in enumerate(self._split_line(line), start=1):
                date = datetime.date(year, month, 1)
                grid.data.append( (date, value) )

        if len(grid.data) != self.numYears*12:
            raise ParseError("Incorrect number of points read from grid {}".format(grid))
        return grid

    def _split_line(self, line):
        """splits line into ints representing individual datavalues given that
        each value is a right aligned int with width 5 characters"""

        #remove newline character
        line = line.rstrip('\n')

        while line:
            chunk = line[:5]
            line = line[5:]
            chunk.lstrip()
            yield int(chunk)

class GridBox():
    """Represents a time series for a single grid box"""

    def __init__(self, xref, yref):
        self.xref = xref
        self.yref = yref
        self.data = []

    def __str__(self):
        return "({},{})".format(self.xref, self.yref)
