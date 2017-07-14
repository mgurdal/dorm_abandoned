"""
Test the fields of the database related objets here
"""
import sys
import unittest
from dorm.database import models
from dorm.database.drivers.sqlite import Sqlite



class FieldTestCase(unittest.TestCase):
    """
        Email field tests
    """

    def setUp(self):
        class TestModel(models.Model):
            """Dummy model"""
            char_test_field = models.Char(max_length=200)

        setattr(self, "TestModel", TestModel)

    def test_char_field(self):
        test_model = self.TestModel(char_test_field="test")
        self.assertEquals(test_model.char_test_field, "test")
