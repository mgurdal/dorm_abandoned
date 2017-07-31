import unittest
from mock import patch, MagicMock
from dorm.database.queries import DeleteQuery, UpdateQuery, SelectQuery
from dorm.database import models


class SqliteDriverTestCase(unittest.TestCase):

    def setUp(self):
