from datetime import datetime
from sqlite3 import OperationalError
from services.restful import ignore_404s, app
from database.drivers import Sqlite
from models import Question, Choice

def main():
    """interact with database"""
    with Sqlite("poll.db") as db:
        try:
            db.create_table(Question)
            db.create_table(Choice)
        except OperationalError:
            pass
        # insert some data
        question = Question(question_text="What is your favorite color?", pub_date=datetime.now())
        question.save()
        choice_1 = Choice(question=question.id, choice_text="green", votes=0)
        choice_2 = Choice(question=question.id, choice_text="yellow", votes=0)
        choice_1.save()
        choice_2.save()

if __name__ == '__main__':
    main()
    app.run()
