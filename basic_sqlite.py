"""
Simple poll app
"""
# built-in
from datetime import datetime
from pprint import pprint
from contextlib import ExitStack

# 3rd party
# import matplotlib.pyplot as plt

# core
from database.drivers.sqlite import Sqlite
from database import models
# from dorm import DORM
from datetime import date, datetime
import config

sq1 = Sqlite({'server_ip': '0.0.0.0', 'database_ip': '127.0.0.1', 'port': '-', 'type': 'sqlite', 'database_name': 'datastore/generated.db', 'user': '-', 'password': '-'})
#sq2 = Sqlite({'server_ip': '0.0.0.0', 'database_ip': '127.0.0.1', 'port': '-', 'type': 'sqlite', 'database_name': 'important_test_2.db', 'user': '-', 'password': '-'})

class Table_2(models.Model):
    __databases__ = [sq1]
    id = models.PrimaryKey()

class Table_3(models.Model):
    __databases__ = [sq1]
    id = models.PrimaryKey()

class Table_1(models.Model):
    __databases__ = [sq1]
    id = models.PrimaryKey()
    char_1 = models.Char(max_length=200)
    varchar_1 = models.Varchar(max_length=200)
    date_1 = models.Date()
    datetime_1 = models.Datetime()
    fk_1 = models.ForeignKey(Table_2)
    mm_1 = models.ManyToMany(Table_3)


# if __name__ == '__main__':

sq1.create_table(Table_2)
sq1.create_table(Table_3)
sq1.create_table(Table_1)

    # sq.drop_table(Table_1_Table_2)
    # dorm = DORM(config)
    # dorm.discover()

t2 = Table_2(id=2)
t2.save(sq1)
t3 = Table_3(id=2)
t3.save(sq1)
t1 = Table_1(id=2, char_1="test_char", varchar_1="test_varchar",
             date_1 = date.today(), datetime_1 = datetime.now(), fk_1 = t2)
t1.save(sq1)
t1 = Table_1(id=1, char_1="test_char_1", varchar_1="test_varchar_2",
             date_1 = date.today(), datetime_1 = datetime.now(), fk_1 = t2)
t1.save(sq1)
t1.mm_1.add(t3)
r = t1.select().all()
l = [x for x in t1.select().all(batch_size=1)]
    # t1t2 = Table_1_Table_2(id=1, table_1=t1, table_2=t2)
    # t1t2.save()
# t1.mm_1.add(t2)
