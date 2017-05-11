"""
Simple poll app
"""

from pprint import pprint
from datetime import datetime
from database.drivers import Sqlite
from database import models

class Question(models.Model):
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

    def __repr__(self):
        return str(vars(self))

class Choice(models.Model):
    question = models.ForeignKeyField(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

    def __repr__(self):
        return str(vars(self))

def main():
    """interact with database"""
    with Sqlite("poll.db") as db:
        try:
            db.create_table(Question)
            db.create_table(Choice)
        except Exception:
            pass
        # insert some data
        question = Question(question_text="What is your favorite color?", pub_date=datetime.now())
        question.save()
        choice_1 = Choice(question=question.id, choice_text="red", votes=0)
        choice_2 = Choice(question=question.id, choice_text="blue", votes=0)
        choice_1.save()
        choice_2.save()

    # read from database
    with Sqlite("poll.db") as db:
        pprint(Question.select().all())
        pprint(Choice.select().all())

if __name__ == '__main__':
    main()
