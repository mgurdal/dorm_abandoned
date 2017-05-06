# coding: utf-8
# %load ORM/database.py



"""
    ORM for sqlite3 like Django ORM.

    Usage:
                >>>from datetime import datetime
                >>>import database

                >>>db = database.Sqlite('blog.db')

                >>>class Post(db.Model):
                ...    title = database.CharField(20)
                ...    content = database.TextField()
                ...    created_time = database.DateTimeField()

                >>>db.create_table(Post)

                >>>post = Post(title='post title', content='post content', created_time=datetime.now())
                >>>post.save()

                >>>post.id, post.title, post.content
                Out: (5, 'post title', 'post content', datetime.datetime(2016, 1, 6, 17, 25, 37, 342000))


                >>>print Post.select().where(id=5).all()
                Out: [<Post post title>]

    The ManyToManyField just like Django ManyToManyField:

                >>>class Tag(db.Model):
                ...    name = database.CharField(50)
                ...    posts = database.ManyToManyField(Post)

    When create table from class `Tag`, ORM will auto-create a table `post_tag` which referenced `Post` and `Tag`.
    We can add tag to the post like this:

                >>>tag = Tag(name='tag')
                >>>tag.save()
                >>>post.tags.add(tag)
                >>>post.tags.all()
                Out: [<Tag tag>]

"""

import sqlite3
import threading


ENCODING_TYPE = 'utf-8'

class Sqlite(threading.local):
    def __init__(self, database):
        super(Sqlite, self).__init__()
        self.database = database
        self.conn = sqlite3.connect(self.database,
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

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

    def execute(self, sql, commit=False):
        cursor = self.conn.cursor()
        print(sql)
        cursor.execute(sql)
        if commit:
            self.commit()
        return cursor


class SelectQuery(object):
    """ select title, content from post where id = 1 and title = "my title";
        select title, content from post where id > 3;
    """

    def __init__(self, model, *args):
        self.model = model
        self.base_sql = 'select {columns} from {tablename};'

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
        cursor = self.model.__db__.execute(sql=sql, commit=True)
        record = cursor.fetchone()
        return record[0]

    def count(self):
        return self._base_function('count')

    def max(self):
        """
        Post.select('id').max()
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
        Post.select().orderby('id', 'desc').all()
        """
        self.base_sql = '{0} order by {1} {2};'.format(self.base_sql.rstrip(';'), column, order)
        return self

    def like(self, pattern):
        """
        Post.select('id').where('content').like('%cont%')
        """
        if 'where' not in self.base_sql:
            raise DatabaseException('Like query must have a where clause before')

        self.base_sql = '{0} like "{1}";'.format(self.base_sql.rstrip(';'), pattern)
        return self

    def _execute(self, sql):
        cursor = self.model.__db__.execute(sql)
        descriptor = list(i[0] for i in cursor.description)
        records = cursor.fetchall()
        query_set = [self._make_instance(descriptor,
                                         map(unicode_str, record)) for record in records]
        return query_set

    def _make_instance(self, descriptor, record):
        try:
            instance = self.model(**dict(zip(descriptor, record)))
        except TypeError:
            return None

        for name, field in instance.__refed_fields__.items():
            if isinstance(field, fields.ForeignKeyReverseField) or isinstance(field, ManyToManyFieldBase):
                field.instance_id = instance.id

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
        return self.model.__db__.execute(sql=self.sql, commit=True)


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
        return self.model.__db__.execute(sql=self.sql, commit=True)


def unicode_str(s):
    return s.encode(ENCODING_TYPE) if isinstance(s, str) else s
