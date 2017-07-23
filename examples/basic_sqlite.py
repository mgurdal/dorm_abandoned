"""
Simple poll app
"""
# built-in
from datetime import datetime
from pprint import pprint
from contextlib import ExitStack

# 3rd party
import matplotlib.pyplot as plt

# core
from dorm.database.drivers.sqlite import Sqlite
from dorm.database import models
# from dorm import DORM
from datetime import date, datetime
import config

sq = Sqlite({'database_name':'important_test.db'})

class Table_2(models.Model):
    id = models.PrimaryKey()

class Table_3(models.Model):
    id = models.PrimaryKey()

class Table_1(models.Model):
    id = models.PrimaryKey()
    char_1 = models.Char(max_length=200)
    varchar_1 = models.VarChar(max_length=200)
    date_1 = models.Date()
    datetime_1 = models.DateTime()
    fk_1 = models.ForeignKey(Table_2)
    mm_1 = models.ManyToMany(Table_3)


#if __name__ == '__main__':
    
sq.create_table(Table_2)
sq.create_table(Table_3)
sq.create_table(Table_1)

    #sq.drop_table(Table_1_Table_2)
    #dorm = DORM(config)
    #dorm.discover()

t2 = Table_2(id=1)
t2.save()
t3 = Table_3(id=1)
t3.save()
t1 = Table_1(id=1, char_1="test_char", varchar_1="test_varchar", date_1=date.today(), datetime_1=datetime.now(), fk_1=t2)
t1.save()
t1.mm_1.add(t3)

    #t1t2 = Table_1_Table_2(id=1, table_1=t1, table_2=t2)
    #t1t2.save()
#t1.mm_1.add(t2)
