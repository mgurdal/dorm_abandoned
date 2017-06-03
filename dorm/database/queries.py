"""
sql queries in here
"""
import gevent

import pandas as pd
import dask.dataframe as dd

from . import models
from config import DATABASES

ENCODING_TYPE = 'utf-8'

def db_job_spawner(sql, db_list, commit=True):
    """
    Usage:
    result = db_job_spawner(db.execute, sql=self.sql, commit=True, db_list)
    """
    jobs = [gevent.spawn(db.execute, sql, commit) for db in db_list]
    result = gevent.joinall(jobs)
    return [job.value for job in jobs]

def unicode_str(s):
    return s.encode(ENCODING_TYPE) if isinstance(s, str) else s

class DatabaseException(Exception):
    """Base database exception"""
    pass

class SelectQuery(object):
    """ select title, content from Question where id = 1 and title = "my title";
        select title, content from Question where id > 3;
    """

    def __init__(self, model, *args):
        self.model = model
        self.base_sql = 'select {columns} from {tablename};'
        self.databases = self.model.__dbs__
        query_args = list(args) if list(args) else ['*']
        self.query = ', '.join([str(column) for column in query_args])

    @property
    def sql(self):
        return self.base_sql.format(
            columns=self.query,
            tablename=self.model.__tablename__
        )

    def all(self):
        return self._execute(self.sql)

    def first(self):
        self.base_sql = '{0} limit 1;'.format(self.base_sql.rstrip(';'))
        return self._execute(self.sql)[0]

    def where(self, *args, **kwargs):
        where_list = []
        for k, v in kwargs.items():
            where_list.append('{0}="{1}"'.format(k, str(v)))
        where_list.extend(list(args))

        self.base_sql = '{0} where {1};'.format(self.base_sql.rstrip(';'), ' and '.join(where_list))
        return self


    def _base_function(self, func):
        sql = self.base_sql.format(
            columns='{0}({1})'.format(func, self.query),
            tablename=self.model.__tablename__
        )
        records = []
        # parallel multi db execute
        for db in self.databases:
            
            cursor = db.execute(sql=sql, commit=True)
            record = cursor.fetchone()
            #print(type(record[0]))
            records += record[0]
        return records
    
    def __getitem__(self, slices):
        """
        Usage:
        #Select N items from all databases
        Question.select()('content')[start:end]
        
        #Select N items from N databases
        Question.select()[start:end, start:end]
        """
        if isinstance(slices, tuple) and all(map(lambda s: isinstance(s, slice), slices)):
            self.databases = self.databases[slices[1]]
            start, end = slices[0].start, slices[0].stop
        elif isinstance(slices, slice):
            start, end = slices.start, slices.stop
        else:
            raise SyntaxError("Invalid slice object")

        if not start: start = 1
        if not end: end = -1    
        self.base_sql = '{0} limit {1} offset {2};'.format(self.base_sql.rstrip(';'), end, start-1)
        return self.all()
            

    def count(self):
        return self._base_function('count')

    def max(self):
        """
        Question.select('id').max()
        """
        return self._base_function('max')

    def min(self):
        return self._base_function('min')

    def avg(self):
        return self._base_function('avg')

    def sum(self):
        return self._base_function('sum')

    def orderby(self, column, order='desc'):
        """
        Question.select().orderby('id', 'desc').all()
        """
        self.base_sql = '{0} order by {1} {2};'.format(self.base_sql.rstrip(';'), column, order)
        return self

    def like(self, pattern):
        """
        Question.select('id').where('content').like('%cont%')
        """
        if 'where' not in self.base_sql:
            raise DatabaseException('Like query must have a where clause before')

        self.base_sql = '{0} like "{1}";'.format(self.base_sql.rstrip(';'), pattern)
        return self


    def as_df(self):
        """Turns sql query result into pandas dataframe"""
        df = pd.read_sql(self.sql, self.databases[0].conn)
        df['database'] = self.databases[0].database

        for new_frame in self.databases[1:]:
            new_piece = pd.read_sql(self.sql, new_frame.conn)
            new_piece['database'] = new_frame.database
            df = df.append(new_piece, ignore_index=True)
            
        df.set_index(df['id'])
        del df['id']
        return df

    def as_ddf(self):
        """Turns pandas dataframe into dask dataframe"""
        df = dd.from_pandas(self.as_df(), npartitions=5)
        return df

    def _execute(self, sql):
        # parallel multi db execute
        
        cursors = [(db.execute(sql), db.database) for db in self.databases] # for
        
        descriptor = list(i[0] for cursor in cursors for i in cursor[0].description)
        jobs = [(gevent.spawn(cursor[0].fetchall), cursor[1]) for cursor in cursors]
        gevent.joinall([x[0] for x in jobs])
        records = [(job[0].value, job[1]) for job in jobs]
        query_set = [self._make_instance(descriptor, map(unicode_str, instance), record[1]) for record in records for instance in record[0]]
        return query_set

    def _make_instance(self, descriptor, record, database):
        
        try:
            
            instance = self.model(**dict(zip(descriptor, record)))
            setattr(instance, "_db", database)
        
        except TypeError:
            return None

        for name, field in instance.__refed_fields__.items():
            if isinstance(field, models.ForeignKeyReverse) or isinstance(field, models.ManyToManyBase):
                field.instance_id = vars(instance)['id']
        return instance


class UpdateQuery(object):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.base_sql = 'update {tablename} set {update_columns};'
        self.update_list = []
        self.where_list = list(*args)
        for k, v in kwargs.items():
            self.where_list.append('{0}="{1}"'.format(k, v))

        if self.where_list:
            self.base_sql = '{0} where {1}'.format(self.base_sql.rstrip(';'), ' and '.join(self.where_list))

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.update_list.append('{0}="{1}"'.format(k, v))
        return self

    @property
    def sql(self):
        return self.base_sql.format(
            tablename=self.model.__tablename__,
            update_columns=' and '.join(self.update_list)
        )

    def commit(self):
        # parallel multi db execute
        return db_job_spawner(self.sql, self.databases, commit=True)
        


class DeleteQuery(object):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.sql = 'delete from {0};'.format(self.model.__tablename__)
        where_list = list(args)
        for k, v in kwargs.items():
            where_list.append('{0}="{1}"'.format(k, v))

        if where_list:
            self.sql = '{0} where {1}'.format(self.sql.rstrip(';'), ' and '.join(where_list))

    def commit(self):
        # parallel multi db execute
        return db_job_spawner(self.sql, self.databases, commit=True)