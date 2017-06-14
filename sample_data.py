
import time
import random
import json
from datetime import datetime
from contextlib import ExitStack

# core
from dorm.database.drivers import Sqlite
from dorm.database import models
from config import DATABASES

from threading import Thread, Lock

class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()
    
def bulk_insert():
    
    for i, data in enumerate(json.loads(open('data.json').read())):
        t = time.time()
        question = Question(question_text=data["question"], pub_date=datetime.now())
        question.save()

        for answer in data["answers"]:
            choice = Choice(question=question,
                                choice_text=answer, votes=random.randint(3, 15))
            choice.save()
        print(i, time.time() - t)

def drop_n_create(db):
    try:
        db.create_table(Question)
        db.create_table(Choice)
    except:
        db.drop_table(Question)
        db.drop_table(Choice)
        db.create_table(Question)
        db.create_table(Choice)  

if __name__ == "__main__":
    with ExitStack() as stack:
        
        dbs = [stack.enter_context(Sqlite(db['address'])) for db in DATABASES]
        #[drop_n_create(db) for db in dbs]
        #bulk_insert()
            