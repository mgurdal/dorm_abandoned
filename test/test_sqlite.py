import unittest
from mock import patch, MagicMock
from dorm.database.queries import DeleteQuery, UpdateQuery, SelectQuery
from dorm.database.drivers.sqlite import Sqlite
from dorm.database import models


class SqliteDriverTestCase(unittest.TestCase):

    def setUp(self):
        dummy_conf = {'server_ip': '0.0.0.0', 'database_ip': '127.0.0.1', 'port': '0',
                      'type': 'test', 'database_name': 'test_db', 'user': 'test', 'password': 'test'}
        self.sqlite_db = Sqlite(dummy_conf)
        self.sqlite_db.conn = MagicMock()


