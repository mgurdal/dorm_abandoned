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

"""
class Employees(models.Model):
    emp_no = models.PrimaryKey()
    birth_date = models.DateTime()
    first_name = models.Char(14)
    last_name = models.Char(16)
    gender = models.Char(1)
    hire_date = models.DateTime()
"""

if __name__ == '__main__':
    dorm = DORM(config)
    dorm.discover()

    def add_some():
        question = Question(id = 500, question_text="What is your favorite color?", pub_date=datetime.now())
        question.save()
        choice = Choice(id = 600, question=question, choice_text="green", votes=0)
        choice.save()

    first_question = Question.select().first()

    all_choices = Choice.select().all()

    # Get first 5 results from all databases
    first_5_choices = Choice.select()[:5]

    # Get first 5 results from first 5 databases
    first_5_choices_of_first_5_dbs = Choice.select()[:5, :5]
