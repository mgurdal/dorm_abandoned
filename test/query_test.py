import os
import unittest
from datetime import datetime
from dorm.database.drivers.sqlite import Sqlite
from dorm.database import models

class QueryTestCase(unittest.TestCase):
    """
        Model based database query tests done here
    """
    def setUp(self):
        """Initialize a db and test model"""
        self.database = Sqlite({'database_name':'memory:'})
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
