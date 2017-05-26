# coding: utf-8

from contextlib import ExitStack

from database import models
from database.drivers import Sqlite
from config import DATABASES

class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

# assuming Question and Choice data already registered in databases    
if __name__ == "__main__":
    with ExitStack() as stack:
        dbs = [stack.enter_context(Sqlite(db['address'])) for db in DATABASES]
        for db in dbs:
            try:
                db.create_table(Question)
                db.create_table(Choice)
            except:
                pass
        # get dask distributed dataframe
        ddf = Choice.select().as_distributed_df()
        result = ddf.votes.value_counts().compute()
        most_common_10_votes = result.sort_values()[-10:]
        print(most_common_10_votes)
