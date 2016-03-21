from itertools import islice
from parse import parse

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
