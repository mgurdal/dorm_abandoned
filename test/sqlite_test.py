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

        self.database.create_table(TestModel) # needs to be mocked
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(TestModel.__tablename__))
        self.assertIsNotNone(cursor.fetchone())

    def test_insert_query(self):
        class TestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()
            text_field = models.Text()
            datetime_field = models.DateTime()

        self.database.create_table(TestModel)

        test_model = TestModel(int_field=1,
                               text_field="test",
                               datetime_field=datetime.now())
        test_model.save()
        self.assertIs(test_model.id, 1)

    def test_insert_query_with_fk(self):
        """Test foreign key relation"""

        class RelatedTestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()

        class TestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()
            foreign_field = models.ForeignKey(RelatedTestModel)

        self.database.create_table(RelatedTestModel)
        self.database.create_table(TestModel)

        related_test_model = RelatedTestModel(int_field=3)
        related_test_model.save()

        test_model = TestModel(int_field=1, foreign_field=related_test_model.id)
        test_model.save()
        self.assertIs(RelatedTestModel.select().first().int_field, 3)

    def test_insert_query_with_many_to_many(self):
        """Test many to many relation"""

        class RelatedTestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()

        class TestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()
            many_field = models.ManyToMany(RelatedTestModel)

        self.database.create_table(RelatedTestModel)
        self.database.create_table(TestModel)

        related_test_model = RelatedTestModel(int_field=3)
        related_test_model.save()

        test_model = TestModel(int_field=1)
        test_model.save()

        test_model.many_field.add(related_test_model)
        self.assertIs(TestModel.many_field.all()[-1].select().first().int_field, 3)

    def test_drop_table(self):
        """
            Table removal test
        """
        class TestModel(models.Model):
            """Dummy class"""
            int_field = models.Integer()
            text_field = models.Text()
            datetime_field = models.DateTime()
        self.database.create_table(TestModel)

        self.database.drop_table(TestModel)
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
        cursor = self.database.execute(query.format(TestModel.__tablename__))
        self.assertIsNone(cursor.fetchone())

    def tearDown(self):
        """
            Clean up
        """
        del self.database


