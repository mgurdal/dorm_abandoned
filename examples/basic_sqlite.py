"""
Simple poll app
"""
# built-in
from datetime import datetime
from pprint import pprint
from contextlib import ExitStack

# 3rd party
import matplotlib.pyplot as plt

# core
from dorm.database.drivers.sqlite import Sqlite
from dorm.database import models
from dorm.main import DORM

import config

class Question(models.Model):
    id = models.PrimaryKey()
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    id = models.PrimaryKey()
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

if __name__ == '__main__':
    dorm = DORM(config)
    dorm.register_model(Choice, Question)
    dorm.discover()

    def add_some():
        question = Question(id = 500, question_text="What is your favorite color?", pub_date=datetime.now())
        question.save()
        choice = Choice(id = 600, question=question, choice_text="green", votes=0)
        choice.save()

    first_question = Question.select()[:1, 11:12]
    all_choices = Choice.select()[:1, :1]

        # Get first 5 results from all databases
        #first_5_choices = Choice.select()[:5]

        # Get first 5 results from first 5 databases
        #first_5_choices_dbs = Choice.select()[:5, :5]

        # Get results as pandas.DataFrame
        #all_choices_as_df = choice.select().as_df()
