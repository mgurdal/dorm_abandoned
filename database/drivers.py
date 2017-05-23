import threading
import sqlite3
import psycopg2
from pymongo import MongoClient
import pandas as pd
from .models import Model, ManyToMany
from utils.serializers import ModelSerializer

class Sqlite(threading.local):
    def __init__(self, database):
        super(Sqlite, self).__init__()
        self.database = database
        self.conn = sqlite3.connect(self.database, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        self.__tables__ = {}
        setattr(self, 'Model', Model)
        if not hasattr(self.Model, "__dbs__"):
            setattr(self.Model, '__dbs__', [])
        self.Model.__dbs__.append(self)
        
    def create_table(self, model):
        tablename = model.__tablename__
        create_sql = ', '.join(field.create_sql() for field in model.__fields__.values())
        self.execute('create table {0} ({1});'.format(tablename, create_sql), commit=True)

        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()

    def drop_table(self, model):
        tablename = model.__tablename__
        self.execute('drop table {0};'.format(tablename), commit=True)
        del self.__tables__[tablename]

        for name, field in model.__refed_fields__.items():
            if isinstance(field, ManyToMany):
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

class MongoDB(threading.local):
    """Not done yet"""
    def __init__(self, database):
        super(MongoDB, self).__init__()
        self.database = MongoClient()[database] # create mongo database
        self.conn = self.database

        self.__tables__ = {}
        setattr(self, 'Model', Model)
        setattr(self.Model, '__db__', self)    
    
    def create_table(self, model):
        tablename = model.__tablename__
        self.database[tablename] # create collection

        # register the given model as a table to database  if  not 
        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model
 
        """ # still do not know what I am supposed to do with relations
        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()
        """
        return tablename
                   
    def drop_table(self, model):
        tablename = model.__tablename__
        # test
        self.database[tablename].drop()
        del self.__tables__[tablename]


    def commit(self):
        # what to do?
        #self.conn.commit()
        pass

    def rollback(self):
        # what to do?
        #self.conn.rollback()
        pass

    def close(self):
        # what
        #self.conn.close()
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # self.close()
        print("exiting now")

    def execute(self, bson, commit=False):
            #print(sql)
            cursor.execute(sql)
            
            return cursor

class Cursor(object):
    
    def __init__(self, conn, query, step=20, forward=0):
        self._conn = conn
        self._query = query
        self._results = []

        self._step = step
        self._forward = forward

    async def execute(self):
        
        cursor = self._conn.execute(self._query)

        if self._forward:
            cursor.forward(self._forward)

        if not cursor:
            raise StopAsyncIteration()
        return cursor

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._cursor is None:
            self._results = await self.execute()

        if not self._results:
            self._forward = self._forward + self._step
            self._results = await self.execute()

        return self._results.pop(0)

class AsyncSqlite(Sqlite):
    def __init__(self, *args, **kwargs):
        super(AsyncSqlite, self).__init__(*args, **kwargs)

    async def execute(self, sql, commit=False):
        cursor = await Cursor(self.conn, sql).execute()
        if commit:
            self.commit()
        return cursor

