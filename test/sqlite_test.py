"""
Test the ORM queries here
"""
import os, sys
import unittest
from datetime import datetime
from dorm.database.drivers.sqlite import Sqlite
from dorm.database import models

class RelatedTestModel(models.Model):
    """Dummy class"""
    int_field = models.Integer()

class TestModel(models.Model):
    """Dummy class"""
    int_field = models.Integer()
    text_field = models.Text()
    datetime_field = models.DateTime()
    foreign_field = models.ForeignKey(RelatedTestModel)

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

        self.database.create_table(RelatedTestModel)
        self.database.create_table(TestModel) # needs to be mocked
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(TestModel.__tablename__))
        self.assertIsNotNone(cursor.fetchone()[0])

    def test_insert_query(self):
            
            test_model = TestModel(int_field=1,
                                text_field="test",
                                datetime_field=datetime.now())
            test_model.save()
            self.assertIs(TestModel.select().where(id=1).first().id, 1)
    def test_insert_query_with_fk(self):
        """Test foreign key relation"""


        c = self.database.execute("SELECT name FROM sqlite_master")
        related_test_model = RelatedTestModel(int_field=3)
        related_test_model.save()

        test_model = TestModel(int_field=1,
                               text_field="test",
                               datetime_field=datetime.now(),
                               foreign_field=related_test_model)
        test_model.save()

        self.assertIs(related_test_model.select().first().int_field, 3)

    
    def test_drop_table(self):
        """
            Table removal test
        """
        self.database.drop_table(RelatedTestModel)
        self.database.drop_table(TestModel)
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(TestModel.__tablename__))
        self.assertIsNone(cursor.fetchone())

    def tearDown(self):
        """
            Clean up
        """
        del self.database


