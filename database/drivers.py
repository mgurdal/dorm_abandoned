import threading
import sqlite3
import pandas as pd
from .models import Model

class Sqlite(threading.local):
    def __init__(self, database):
        super(Sqlite, self).__init__()
        self.database = database
        self.conn = sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        self.__tables__ = {}
        setattr(self, 'Model', Model)
        setattr(self.Model, '__db__', self)

    def create_table(self, model):
        tablename = model.__tablename__
        create_sql = ', '.join(field.create_sql() for field in model.__fields__.values())
        self.execute('create table {0} ({1});'.format(tablename, create_sql), commit=True)

        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToManyField):
                field.create_m2m_table()

    def drop_table(self, model):
        tablename = model.__tablename__
        self.execute('drop table {0};'.format(tablename), commit=True)
        del self.__tables__[tablename]

        for name, field in model.__refed_fields__.items():
            if isinstance(field, ManyToManyField):
                field.drop_m2m_table()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def execute(self, sql, commit=False):
        cursor = self.conn.cursor()
        #print(sql)
        cursor.execute(sql)
        if commit:
            self.commit()
        return cursor