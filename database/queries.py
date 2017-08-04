"""
sql queries in here
"""

import gevent


from . import models

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

    def __init__(self, model, *args, target_databases=[]):
        self.model = model.__class__
        self.base_sql = 'select {columns} from {tablename};'
        self.databases = target_databases if target_databases else self.model.__databases__
        query_args = list(args) if list(args) else ['*']
        self.query = ', '.join([str(column) for column in query_args])

    @property
    def sql(self):
        return self.base_sql.format(
            columns=self.query,
            tablename=self.model.__tablename__
        )

    def all(self, datatype=None, batch_size=None):

        return self._execute(self.sql, datatype=datatype, batch_size=batch_size)

    def first(self, datatype=None):
        self.base_sql = '{0} limit 1;'.format(self.base_sql.rstrip(';'))
        try:
            return next(self._execute(self.sql, datatype=datatype))
        except Exception as e:
            raise e

    def where(self, *args, **kwargs):
        where_list = []  # might need to add validation
        for k, v in kwargs.items():
            where_list.append('{0}={1}'.format(k, str(v)))
        where_list.extend(list(args))

        self.base_sql = '{0} where {1};'.format(
            self.base_sql.rstrip(';'), ' and '.join(where_list))
        return self

    def _base_function(self, func):
        # support custom functions

        # this logic might be wrong, might need
        # to apply function for each selected column
        sql = self.base_sql.format(
            columns='{0}({1})'.format(func, self.query),
            tablename=self.model.__tablename__
        )
        records = []
        # parallel multi db execute
        for db in self.databases:
            cursor = db.execute(sql=sql, commit=True)
            record = cursor.fetchone()
            # print(type(record[0]))
            records += record
        return records

    # this method is really important
    def __getitem__(self, slices):
        """
        Usage:
        #Select N items from all databases
        Question.select()('content')[start:end]

        #Select N items from N databases
        Question.select()[start:end, start:end]
        """

        if isinstance(slices, tuple) and all(map(lambda s: isinstance(s, slice), slices)):
            # reduce the databases based on the first slice
            self.databases = self.databases[slices[0]]
            # reduce the query based on second slice
            first_slice, second_slice = slices[1].start, slices[1].stop
        elif isinstance(slices, slice):
            first_slice, second_slice = slices.start, slices.stop
        else:
            raise SyntaxError("Invalid slice object")

        start = first_slice if first_slice else 1
        end = second_slice if second_slice else -1

        self.base_sql = '{0} limit {1} offset {2};'.format(
            self.base_sql.rstrip(';'), end, start - 1)
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
        self.base_sql = '{0} order by {1} {2};'.format(
            self.base_sql.rstrip(';'), column, order)
        return self

    def like(self, pattern):
        """
        Question.select('id').where('content').like('%cont%')
        """
        if 'where' not in self.base_sql:
            raise DatabaseException(
                'Like query must have a where clause before')
        # this query might be wrong
        self.base_sql = '{0} like {1};'.format(
            self.base_sql.rstrip(';'), pattern)
        return self

    def as_df(self):
        import pandas as pd
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

        """def as_ddf(self):
        Turns pandas dataframe into dask dataframe
        df = dd.from_pandas(self.as_df(), npartitions=5)
        return df"""

    # hard to test, needs refactor
    def _execute(self, sql, datatype=dict, batch_size=None):
        cursors = []

        for db in self.databases:
            cursor = db.execute(sql)
            cursors.append(cursor)
            description = [des[0] for des in cursor.description]

            def get_cursor(batch_size):
                if batch_size:
                    next_batch = cursor.fetchmany(batch_size)
                    while next_batch:
                        yield next_batch
                        next_batch = cursor.fetchmany(batch_size)
                else:
                    yield cursor.fetchall()
            # fetch data with cunks
            records = cursor.fetchall()  # if not batch_size else cursor.fetchmany(batch_size)
            for record in records:  # get_cursor(batch_size):
                #model = None
                if not datatype:
                    model = self.model(**dict(zip(description, record)))
                    model.conf = db.conf
                    yield model
                elif datatype == dict:
                    model = dict(zip(description, record))
                    model['conf'] = db.conf
                    yield model
                else:
                    raise Exception("Unsupported result type")

    def _make_instance(self, descriptor, record):

        try:
            instance = self.model(**dict(zip(descriptor, record)))
        except TypeError as e:
            raise e

    def _handle_refered_fields(self, instance):
        for _, field in instance.__refered_fields__.items():
            if isinstance(field, models.ForeignKeyReverse) or isinstance(field, models.ManyToManyBase):
                # implement  nested query
                field.instance_id = vars(instance)['id']
        return instance


class UpdateQuery(object):
    def __init__(self, model, **kwargs):
        assert 'update_fields' in kwargs, "Please define the fields you want to update. e.g update_fields=[{name:mehmet}]"
        assert 'where_fields' in kwargs, "Please specify in which fields you want to update. e.g where_fields=[{id:1}]"
        self.model = model
        self.base_sql = 'update {tablename} set {update_columns};'
        self.update_fields = kwargs['update_fields']  # is this have a cost?
        self.where_fields = kwargs['where_fields']

        self.update_list = ['{0}={1}'.format(
            k, v) for k, v in self.update_fields.items()]
        self.where_list = ['{0}={1}'.format(k, v)
                           for k, v in self.where_fields.items()]

        self.base_sql = '{0} where {1};'.format(self.base_sql.rstrip(';'),
                                                'and '.join(self.where_list)
                                                )

    def set(self, **kwargs):
        for k, v in kwargs.items():
            # ignore if field already defined in update list
            if self.update_fields.get(k) == v:
                continue
            self.update_list.append('{0}={1}'.format(k, v))
        return self

    @property
    def sql(self):
        return self.base_sql.format(
            tablename=self.model.__tablename__,
            update_columns=' and '.join(self.update_list)
        )

    def commit(self):
        # parallel multi db execute
        return db_job_spawner(self.sql, self.model.__databases__, commit=True)


class DeleteQuery(object):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.sql = 'delete from {0};'.format(self.model.__tablename__)
        where_list = list(args)
        for k, v in kwargs.items():
            where_list.append('{0}={1}'.format(k, v))

        if where_list:
            self.sql = '{0} where {1};'.format(
                self.sql.rstrip(';'), ' and '.join(where_list))

    def commit(self):
        # parallel multi db execute
        return db_job_spawner(self.sql, self.model.__databases__, commit=True)
