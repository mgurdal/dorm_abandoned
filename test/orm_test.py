"""
Test the ORM queries here
"""
import os
import unittest
from datetime import datetime
from database.drivers import Sqlite
from database import models

class ModelTestCase(unittest.TestCase):
    """
        ORM ultility tests
    """

    def setUp(self):
        """
            Code setup
        """
        self.database = Sqlite(':memory:')

    def test_create_table(self):
        """
            table creation test
        """
        class TestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()
            text_field = models.Text()
            datetime_field = models.DateTime()

        self.test_model = TestModel(int_field=1,
                                    text_field="some_text",
                                    datetime_field=datetime.now())
        self.database.create_table(TestModel) # needs to be mocked
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(TestModel.__tablename__))
        self.assertIsNotNone(cursor.fetchone())

    def test_drop_table(self):
        """
            Table removal test
        """
        self.test_create_table()
        self.database.drop_table(self.test_model) # needs to be mocked
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(self.test_model.__tablename__))
        self.assertIsNone(cursor.fetchone())

    def tearDown(self):
        """
            Clean up
        """
        del self.database


class QueryTestCase(unittest.TestCase):
    """
        Model based database query tests done here
    """
    def setUp(self):
        """Initialize a db and test model"""
        self.database = Sqlite(':memory:')
        class TestModel(models.Model):
            """Dummy class"""
            test_int = models.Integer()
            test_text = models.Text()
            test_datetime = models.DateTime()
        self.database.create_table(TestModel)
        self.test_model = TestModel(test_int=1, test_text="some_text", test_datetime=datetime.now())
        self.test_model.save()
        
    def test_select_query(self):
        sample = self.test_model.select().first()
        self.assertIsInstance(sample, self.test_model.__class__)

    def tearDown(self):
        del self.test_model
        del self.database


if __name__ == '__main__':
    unittest.main()
