"""SQLite Drivers"""

import sqlite3
from .base import BaseDriver

class Sqlite(BaseDriver):
    """SQLite Driver"""
    def __init__(self, database):
        super(Sqlite, self).__init__(database=database,
                                     adapter=sqlite3,
                                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
