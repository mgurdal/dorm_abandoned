"""
Test the ORM queries here
"""
import os
import unittest
from ..database.queries import Sqlite
from ..database.models import Model
from ..database.fields import IntegerField, TextField, DateTimeField

class TableTestCase(unittest.TestCase):
    """
        ORM ultility tests
    """

    def setUp(self):
        """
            Code setup
        """
        self.database = Sqlite('test.db')

    def test_create_table(self):
        """
            table creation test
        """
        class TestModel(Model):
            """Dummy class"""
            test_int = IntegerField()
            test_text = TextField()
            test_datetime = DateTimeField()

        self.table = TestModel()
        self.database.create_table(TestModel) # needs to be mocked
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(TestModel.__tablename__))
        self.assertIsNotNone(cursor.fetchone())

    def test_drop_table(self):
        """
            Table removal test
        """
        self.test_create_table()
        self.database.drop_table(self.table) # needs to be mocked
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(self.table.__tablename__))
        self.assertIsNone(cursor.fetchone())

    def tearDown(self):
        """
            Clean up
        """
        del self.database
        os.remove("test.db") # needs to be mocked


class QueryTestCase(unittest.TestCase):
    """
        Model based database query tests done here
    """

if __name__ == '__main__':
    unittest.main()
