"""
Test the fields of the database related objets here
"""
import re
import unittest
from database import models
from database.drivers import Sqlite

class TestModel(models.Model):
    """Dummy model"""
    email_field = models.Email(max_length=200)

class EmailTestCase(unittest.TestCase):
    """
        Email field tests
    """

    def setUp(self):
        email_pattern = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        self.prog = re.compile(email_pattern, re.X)
        self.db = Sqlite(":memory:")

    def test_correct_email(self):
        test_model = TestModel(email_field="mgurdal@protonmail.com")
        test_model.save()
        tm = TestModel.select().first()
        result = self.prog.match(tm.email_field)
        
