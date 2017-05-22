# coding: utf-8
from database import models
from database.drivers import Sqlite

class Question(models.Model):
        question_text = models.Char(max_length=200)
        pub_date = models.DateTime()

with Sqlite("poll_1.db") as db, Sqlite("poll_2.db") as db2:
        dota = Question.select().as_df()
        dota2= Question.select().as_distributed_df()
