""" test sqlite driver here """
import unittest
from unittest.mock import MagicMock
from drivers.sqlite import Sqlite

class SqliteDriverTestCase(unittest.TestCase):
    """ test sqlite driver here """

    def setUp(self):
        conf = {'database_name':':memory:'}
        self.sq = MagicMock(Sqlite(conf))
    
        
