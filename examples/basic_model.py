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
from dorm.database.drivers import Sqlite
from dorm.database import models
from config import DATABASES

class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

if __name__ == '__main__':
    with ExitStack() as stack:
        dbs = [stack.enter_context(Sqlite(db['address'])) for db in DATABASES]
        for db in dbs:
            try:
                db.create_table(Question)
                db.create_table(Choice)
            except:
                pass

        # insert some data
        #question = Question(question_text="What is your favorite color?", pub_date=datetime.now())
        #question.save()

        #choice = Choice(question=question, choice_text="green", votes=0)
        #choice.save()

        #first_question = question.select().first()
        #all_choices = Choice.select().all()

        # Get first 5 results from all databases
        #first_5_choices = Choice.select()[:5]

        # Get first 5 results from first 5 databases
        #first_5_choices_dbs = Choice.select()[:5, :5]

        # Get results as pandas.DataFrame
        #all_choices_as_df = choice.select().as_df()
