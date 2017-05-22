import os
import unittest
from datetime import datetime

from pymongo import MongoClient

from database import models
from database.drivers import Sqlite, MongoDB

class Question(models.MongoModel): # MongoModel
    """Mongo model """
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.MongoModel):
    """Mongo model with another model inside"""
    question = Question()
    choice_text = models.Char(max_length=200)
    votes = models.Integer()


class MongoDriverTestCase(unittest.TestCase):
    """Test the mongodb connection driver here"""
    
    def setUp(self):
        self.client = MongoClient()
        
    def test_database_and_table_creation(self):
        db = MongoDB("mongo_test")
        self.assertTrue(self.client.get_database("mongo_test"))

    def test_table_creation(self):
        db = MongoDB("mongo_test")

        question_tname = db.create_table(Question)
        choice_tname = db.create_table(Choice)
        self.assertTrue(self.client.mongo_test[question_tname])
        self.assertTrue(self.client.mongo_test[choice_tname])

    def test_save_model(self):
        test_question = Question(question_text="which test?", pub_date=datetime.now())
        test_question.save()
        test_choice = Choice(question=test_question, choice_text="mongo test", votes=0)
        test_choice.save()
        
        """def test_insert_into_table(self):
        # insert some data
        question = Question(question_text="What is your favorite color?", pub_date=datetime.now())
        question.save()
        choice_1 = Choice(question=question.id, choice_text="red", votes=0)
        choice_2 = Choice(question=question.id, choice_text="blue", votes=0)
        choice_1.save()
        choice_2.save()"""

        def tearDown(self):
            self.test_collection.drop()
            self.test_db.dropDatabase()
            self.client.close()
            del self.client
            del self.test_db
            del self.test_collection
            