# coding: utf-8
from database import models
from database.drivers import Sqlite
import matplotlib.pyplot as plt

class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

# assuming Question and Choice data already registered in databases    
with Sqlite("poll_1.db"), Sqlite("poll_2.db"):
    # get dask distributed dataframe
    ddf = Choice.select().as_distributed_df()
    result = ddf.votes.value_counts().compute()
    most_common_10_votes = result.sort_values()[-10:]
    print(most_common_10_votes)
