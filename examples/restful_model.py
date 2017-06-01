"""
Simple poll app with RESTful service
"""

import json
from datetime import datetime
from contextlib import ExitStack

from dorm.database import models
from dorm.database.drivers import Sqlite
from dorm.services.restful import rest, app

from config import DATABASES

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
        dbs = [stack.enter_context(Sqlite(db['address'])) for db in DATABASES[:400]]
        for db in dbs:
            try:
                db.create_table(Question)
                db.create_table(Choice)
            except:
                pass
        app.run()
