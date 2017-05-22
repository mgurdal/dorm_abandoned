"""
Simple poll app with RESTful service
"""
from datetime import datetime
from database import models
from services.restful import rest, app

@rest()
class Question(models.Model):
    id = models.PrimaryKey()
    question_text = models.Char(max_length=200)
    pub_date = models.DateTime()

    def __repr__(self):
        return str(vars(self))

@rest(methods=["post", "delete", "patch"])
class Choice(models.Model):
    id = models.PrimaryKey()
    question = models.ForeignKey(Question)
    choice_text = models.Char(max_length=200)
    votes = models.Integer()

    def __repr__(self):
        return str(vars(self))

if __name__ == "__main__":
    app.run()
