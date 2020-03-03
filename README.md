Code example for JBA job application

## Usage
    ./main.py [-h] [-t TABLE_NAME] [-d DATABASE] [-b BATCH] [-a] [-v] FILE

    Read data from file, transform and store in a database.

    positional arguments:
      FILE                  File to read data from

    optional arguments:
      -h, --help            show help message and exit
      -t TABLE_NAME, --table-name TABLE_NAME
                            Name of the database table to store data in. If not
                            provided a table name will be computed from the header
                            of FILE
      -d DATABASE, --database DATABASE
                            Specifies the database to use in SQLAlchemy URI form,
                            default is 'sqlite:///FILE.db'
      -b BATCH, --batch BATCH
                            Batch size for inserts into the database. Too low a
                            value can cause performance issues, too high a value
                            may cause errors depending on the driver used.
                            Defaults to 120,000 (1000 grid boxes worth of data for
                            a 10 year file)
      -a, --append          Allows data to be appended to an existing table. If
                            not set the table will be dropped and recreated if it
                            already exists
      -v, --verbose         Causes generated SQL statements to be echoed to stderr
                            for debugging purposes

## Requirements

Minimal requirements are listed in Requirements.txt, to install requirements using pip use:

    pip install -r Requirements.txt

If a database engine other than sqlite3 from the python standard library is
used the relevent python database driver may also be required.
