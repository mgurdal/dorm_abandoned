
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


encoding_type = 'utf-8'


class Field(object):
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None

    def create_sql(self):
        """Return sql statement for create table."""
        return '"{0}" {1}'.format(self.name, self.column_type)


class IntegerField(Field):
    def __init__(self):
        super(IntegerField, self).__init__('INTEGER')

    def sql_format(self, data):
        return str(int(data))


class CharField(Field):
    def __init__(self, max_lenth=255):
        self.max_lenth = max_lenth
        super(CharField, self).__init__('VARCHAR')

    def create_sql(self):
        return '"{0}" {1}({2})'.format(self.name, self.column_type, self.max_lenth)

    def sql_format(self, data):
        return '"{0}"'.format(str(data))


class TextField(Field):
    def __init__(self):
        super(TextField, self).__init__('TEXT')

    def sql_format(self, data):
        return '"{0}"'.format(str(data))


class DateTimeField(Field):
    def __init__(self):
        super(DateTimeField, self).__init__('DATETIME')

    def sql_format(self, data):
        return '"{0}"'.format(data.strftime('%Y-%m-%d %H:%M:%S'))


class PrimaryKeyField(IntegerField):
    def __init__(self):
        super(PrimaryKeyField, self).__init__()

    def create_sql(self):
        return '"{0}" {1} NOT NULL PRIMARY KEY'.format(self.name, self.column_type)


class ForeignKeyField(IntegerField):
    def __init__(self, to_table):
        self.to_table = to_table
        super(ForeignKeyField, self).__init__()

    def create_sql(self):
        return '{column_name} {column_type} NOT NULL REFERENCES "{tablename}" ("{to_column}")'.format(
            column_name=self.name,
            column_type=self.column_type,
            tablename=self.to_table,
            to_column='id'
        )


class ForeignKeyReverseField(object):
    def __init__(self, from_table):
        self.from_table = from_table
        self.name = None
        self.tablename = None
        self.instance_id = None
        self.db = None
        self.from_model = None
        self.relate_column = None

    def update_attr(self, name, tablename, db):
        self.name = name
        self.tablename = tablename
        self.db = db
        self.from_model = self.db.__tables__[self.from_table]
        for k, v in self.from_model.__dict__.items():
            if isinstance(v, ForeignKeyField) and v.to_table == self.tablename:
                self.relate_column = k

    def all(self):
        return self._query_sql().all()

    def count(self):
        return self._query_sql().count()

    def _query_sql(self):
        return self.from_model.select().where(**{self.relate_column: self.instance_id})


class ManyToManyFieldBase(object):
    def __init__(self, to_model):
        self.to_model = to_model

        self.name = None
        self.tablename = None
        self.db = None

        self.instance_id = None

        self.relate_model = None
        self.relate_table = None
        self.relate_column = None
        self.to_table = None
        self.to_column = None

    def update_attr(self, name, tablename, db):
        self.name = name
        self.tablename = tablename
        self.db = db

    def add(self, to_instance):
        insert = {
            self.relate_column: self.instance_id,
            self.to_column: to_instance.id
        }
        self.relate_model(**insert).save()

    def remove(self, to_instance):
        self.relate_model.delete(**{self.to_column: to_instance.id}).commit()

    def all(self):
        return self._query_sql().all()

    def count(self):
        return self._query_sql().count()

    def _query_sql(self):
        self.to_model = self.db.__tables__[self.to_table]

        relate_instances = self.relate_model.select().where(**{self.relate_column: self.instance_id}).all()
        to_ids = [str(getattr(instance, self.to_column)) for instance in relate_instances]
        where_sql = 'id in ({0})'.format(', '.join(to_ids))

        return self.to_model.select().where(where_sql)


class ManyToManyField(ManyToManyFieldBase):
    def __init__(self, to_model):
        super(ManyToManyField, self).__init__(to_model)

    def update_attr(self, name, tablename, db):
        super(ManyToManyField, self).update_attr(name, tablename, db)
        if self.to_model not in self.db.__tables__.values():
            raise DatabaseException('Related table "{0}" not exists'.format(self.to_model.__tablename__))

        self.to_table = self.to_model.__tablename__
        self.to_column = '{0}_id'.format(self.to_table)
        self.relate_column = '{0}_id'.format(self.tablename)

        class_name = '{0}_{1}'.format(self.to_table, self.tablename)
        class_attrs = {
            self.relate_column: ForeignKeyField(self.tablename),
            self.to_column: ForeignKeyField(self.to_table)
        }
        m2m_model = type(class_name, (Model, ), class_attrs)

        self.relate_model = m2m_model
        self.relate_table = getattr(m2m_model, '__tablename__')
        self.db.__tables__[self.relate_table] = m2m_model
        self.create_reversed_field()

    def create_m2m_table(self):
        self.db.create_table(self.relate_model)
        self.create_reversed_field()

    def drop_m2m_table(self):
        try:
            table_model = self.db.__tables__[self.relate_table]
        except KeyError:
            raise DatabaseException('Can not drop this table: "{0}" not exists'.format(self.relate_table))
        self.db.drop_table(table_model)
        self.delete_reversed_field()

    def create_reversed_field(self):
        field = ManyToManyFieldBase(self.db.__tables__[self.tablename])
        field.db = self.db
        field.name = '{0}s'.format(self.tablename)
        field.to_table, field.tablename = self.tablename, self.to_table
        field.to_column, field.relate_column = self.relate_column, self.to_column
        field.relate_model, field.relate_table = self.relate_model, self.relate_table

        setattr(self.to_model, field.name, field)
        self.to_model.__refed_fields__[field.name] = field

    def delete_reversed_field(self):
        to_column = '{0}s'.format(self.tablename)
        delattr(self.to_model, to_column)
        del self.to_model.__refed_fields__[to_column]


class MetaModel(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return super(MetaModel, mcs).__new__(mcs, name, bases, attrs)

        cls = super(MetaModel, mcs).__new__(mcs, name, bases, attrs)

        if 'Meta' not in attrs.keys() or not hasattr(attrs['Meta'], 'db_table'):
            setattr(cls, '__tablename__', name.lower())
            print(name.lower())
        else:
            setattr(cls, '__tablename__', attrs['Meta'].db_table)
            

        if hasattr(cls, '__db__'):
            getattr(cls, '__db__').__tables__[cls.__tablename__] = cls
        else:
            print("could not find name")
        fields = {}
        refed_fields = {}
        has_primary_key = False
        for field_name, field in cls.__dict__.items():
            if isinstance(field, ForeignKeyReverseField) or isinstance(field, ManyToManyField):
                field.update_attr(field_name, cls.__tablename__, cls.__db__)
                refed_fields[field_name] = field
            if isinstance(field, Field):
                field.name = field_name
                fields[field_name] = field
                if isinstance(field, PrimaryKeyField):
                    has_primary_key = True

        if not has_primary_key:
            pk = PrimaryKeyField()
            pk.name = 'id'
            fields['id'] = pk

        setattr(cls, '__fields__', fields)
        setattr(cls, '__refed_fields__', refed_fields)
        return cls


class DatabaseException(Exception):
    pass


class Model(metaclass=MetaModel):
    __metaclass__ = MetaModel

    def __init__(self, **kwargs):
        for name, field in kwargs.items():
            if name not in self.__fields__.keys():
                raise DatabaseException('Unknown column: {0}'.format(name))
            setattr(self, name, field)

        super(Model, self).__init__()

    @classmethod
    def get(cls, **kwargs):
        return SelectQuery(cls).where(**kwargs).first()

    @classmethod
    def select(cls, *args):
        return SelectQuery(cls, *args)

    @classmethod
    def update(cls, *args, **kwargs):
        return UpdateQuery(cls, *args, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        return DeleteQuery(cls, *args, **kwargs)

    def save(self):
        base_query = 'insert into {tablename}({columns}) values({items});'
        columns = []
        values = []
        for field_name, field_model in self.__fields__.items():
            if hasattr(self, field_name) and not isinstance(getattr(self, field_name), Field):
                columns.append(field_name)
                values.append(field_model.sql_format(getattr(self, field_name)))

        sql = base_query.format(
            tablename=self.__tablename__,
            columns=', '.join(columns),
            items=', '.join(values)
        )
        cursor = self.__db__.execute(sql=sql, commit=True)
        self.id = cursor.lastrowid

        for name, field in self.__refed_fields__.items():
            if isinstance(field, ForeignKeyReverseField) or isinstance(field, ManyToManyFieldBase):
                field.instance_id = self.id


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
        query_set = [self._make_instance(descriptor, map(unicode_str, record)) for record in records]
        return query_set

    def _make_instance(self, descriptor, record):
        try:
            instance = self.model(**dict(zip(descriptor, record)))
        except TypeError:
            return None

        for name, field in instance.__refed_fields__.items():
            if isinstance(field, ForeignKeyReverseField) or isinstance(field, ManyToManyFieldBase):
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
    return s.encode(encoding_type) if isinstance(s, str) else s

class Category(Model):
    """ Blog categories """
    name = CharField(max_lenth=255)

class Post(Model):
    title = CharField(max_lenth=255)
    body = TextField()
    category = ManyToManyField(Category)
    creation_date = DateTimeField()

if __name__ == "__main__":
    DB = Sqlite("blog.db")
    DB.create_table(Post)