import unittest
from mock import patch, MagicMock
from dorm.database import models

class MetaModelTestCase(unittest.TestCase):
    """Base field object"""

    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_db.__tables__ = {}

        self.model = models.MetaModel('TestModel', (object,), {
            '__databases__': [self.mock_db, ]})

    

    def test_metamodel_generates_a_model_correctly(self):
        model = self.model

        self.assertIsNotNone(model)
        self.assertIn('__fields__', model.__dict__.keys())
        self.assertIn('__refered_fields__', model.__dict__.keys())
        self.assertIn('testmodel', self.mock_db.__tables__.keys())

        
