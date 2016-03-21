from itertools import islice
from parse import parse
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
                "{} file created on {} at {} by {}",
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

    @property
    def numYears(self):
        """Gets the number of years the data set encompases"""
        if not self._header_read:
            raise ValueError("numYears has no value until read_header() is called")
        return self.maxYear - self.minYear + 1

    def gridboxes(self):
        """Returns an iterator of GridBoxes from the current file"""
        
        #make sure header is read
        self.read_header()
        
        counter = 0
        line = self._file.readline()
        while line:
            counter += 1
            grid_header = parse("Grid-ref={xref:>d},{yref:>d}", line)
            if not grid_header:
                raise ParseException("Error parsing Grid Box header for Grid Box #{}".format(counter))
            yield self.read_gridbox_data(**grid_header.named)

            line = self._file.readline()

        if counter != self.numBoxes:
            raise ParseError("Expected {} Boxes, found {}".format(self.numBoxes, counter))

    def read_gridbox_data(self, xref, yref):
        """Reads the data for a grid box from file and returns it contained in
        a GridBox"""

        class GridBox():
            """Represents a time series for a single grid box"""

            def __init__(self, xref, yref):
                self.xref = xref
                self.yref = yref
                self.data = []

        grid = GridBox(xref, yref)
        for year in range(self.minYear, self.maxYear + 1):
            line = self._file.readline()
            for month, value in enumerate(map(int, line.split()), start=1):
                date = datetime.date(year, month, 1)
                grid.data.append( (date, value) )

        return grid
