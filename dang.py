# coding: utf-8
from database.drivers import Sqlite
from database import models

db = Sqlite("test.db")

class P(models.Model):
    text = models.Text()
 
p = P(text="some text")
p.save()
p.select().first()
