"""
Simple poll app with RESTful service
"""
from datetime import datetime
from database import models
from database.drivers import Sqlite
from services.restful import rest, app
from contextlib import ExitStack
from config import DATABASES
import json

@rest()
class Question(models.Model):
    id = models.PrimaryKey()
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()


@rest(methods=["post", "delete", "patch"])
class Choice(models.Model):
    id = models.PrimaryKey()
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

if __name__ == "__main__":
    ## Multiple Database Connection & Parallel Processing
    with ExitStack() as stack:
        [stack.enter_context(Sqlite(db['address'])) for db in DATABASES]
        app.run()
