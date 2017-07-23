
import sys
import time
import json
from sqlite3 import OperationalError

from dorm.database.queries import *
from dorm.utils.serializers import jsonify

"""
Create Field based classes here to represent the database columns
"""

class Field(object):
    """Base field object"""
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None

    def create_sql(self):
        """Return sql statement for create table."""
        return '{0} {1}'.format(self.name, self.column_type)

    def _serialize_data(self, data):
        return data.encode()

class Integer(Field):
    """SQLite Integer field"""
    def __init__(self):
        super(Integer, self).__init__('INTEGER')

    def sql_format(self, data):
        """sql query format of data"""
        return str(int(data))
    
    def _serialize_data(self, data):
        return data

class Float(Field):
    """SQLite Float field"""
    def __init__(self):
        super(Float, self).__init__('DOUBLE')

    def sql_format(self, data):
        """sql query format of data"""
        return str(int(data))
    
    def _serialize_data(self, data):
        return data

class Char(Field):
    """SQLite Char field"""
    def __init__(self, max_length=255):
        self.max_length = max_length
        super(Char, self).__init__('CHAR')

    def create_sql(self):
        return '{0} {1}({2})'.format(self.name, self.column_type, self.max_length)

    def sql_format(self, data):
        """sql query format of data"""
        if len(data) > self.max_length:
            raise Exception('maximum length exceeded')
        return "'{0}'".format(str(data))

class VarChar(Field):
    """SQLite Varchar field"""
    def __init__(self, max_length=255):
        self.max_length = max_length
        super(VarChar, self).__init__('VARCHAR')

    def create_sql(self):
        return '{0} {1}({2})'.format(self.name, self.column_type, self.max_length)

    def sql_format(self, data):
        """sql query format of data"""
        return "'{0}'".format(str(data))
    
class Text(Field):
    """SQLite Text field"""
    def __init__(self):
        super(Text, self).__init__('TEXT')

    def sql_format(self, data):
        """sql query format of data"""
        return "'{0}'".format(str(data))

class DateTime(Field):
    def __init__(self):
        super(DateTime, self).__init__('DATETIME')

    def sql_format(self, data):
        return "'{0}'".format(str(data))
    
    def _serialize_data(self, data):
        return str(data)
    
    def __str__(self, data, format='%Y-%m-%d %H:%M:%S.%f'):
        return data.strftime(format)

class Date(Field):
    def __init__(self):
        super(Date, self).__init__('DATE')

    def sql_format(self, data):
        return "'{0}'".format(str(data))
    
    def _serialize_data(self, data):
        return str(data)
    
    def __str__(self, data, format='%Y-%m-%d'):
        return data.strftime(format)

class Timestamp(Field):
    def __init__(self):
        super(Timestamp, self).__init__('TIMESTAMP')

    def sql_format(self, data):
        return "'{0}'".format(self.to_string(data))
    
    def _serialize_data(self, data):
        return str(data)

    def __str__(self, data, format='%Y-%m-%d %H:%M:%S'):
        return data.strftime(format)


class PrimaryKey(Integer):
    def __init__(self):
        super(PrimaryKey, self).__init__()

    def create_sql(self):
        return '{0} {1} NOT NULL PRIMARY KEY'.format(self.name, self.column_type)

class ForeignKey(Integer):
    def __init__(self, to_table):
        self.to_table = to_table
        super(ForeignKey, self).__init__()

    def create_sql(self):
        return '{column_name} {column_type} NOT NULL REFERENCES "{tablename}" ("{to_column}")'.format(
            column_name=self.name,
            column_type=self.column_type,
            tablename=self.to_table,
            to_column='id'
        )

    def sql_format(self, data):
        """sql query format of data"""
        if isinstance(data, Model):
            return str(data.id) # find the pk
        else:
            return super(ForeignKey, self).sql_format(data)

    def _serialize_data(self, data):
        """ not done yet -> serialize the given model """
        return data

class ForeignKeyOld(Field):
    def __init__(self, to_table):
        self.to_table = to_table
        self.table_name = to_table.__tablename__
        
        super(ForeignKey, self).__init__('INTEGER')

    def create_sql(self):
        fk_sql = '{column_name} {column_type} NOT NULL REFERENCES {tablename} ({to_column})'.format(
            column_name=self.name,
            column_type=self.column_type,
            tablename=self.table_name,
            to_column='id'
        )
        return fk_sql

    def sql_format(self, data):
        """sql query format of data"""
        return "'{0}'".format(str(data.id))  

    def _serialize_data(self, data):
        """ not done yet -> serialize the given model """
        return data
    
class ForeignKeyReverse(object):
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
        self.from_model = self.db.__tables__[self.from_table.__tablename__]
        for k, v in self.from_model.__dict__.items():
            if isinstance(v, ForeignKey) and v.to_table == self.tablename:
                self.relate_column = k

    def all(self):
        return self._query_sql().all()

    def count(self):
        return self._query_sql().count()

    def _query_sql(self):
        return self.from_model.select().where(**{self.relate_column: self.instance_id})


class ManyToManyBase(object):
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


class ManyToMany(ManyToManyBase):
    def __init__(self, to_model):
        super(ManyToMany, self).__init__(to_model)

    def update_attr(self, name, tablename, db):
        super(ManyToMany, self).update_attr(name, tablename, db)
        if self.to_model not in self.db.__tables__.values():
            raise DatabaseException('Related table "{0}" not exists'.format(self.to_model.__tablename__))

        self.to_table = self.to_model.__tablename__
        self.to_column = '{0}_id'.format(self.to_table)
        self.relate_column = '{0}_id'.format(self.tablename)

        class_name = '{0}_{1}'.format(self.to_table, self.tablename)
        class_attrs = {
            self.relate_column: ForeignKey(self.tablename),
            self.to_column: ForeignKey(self.to_table)
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
        field = ManyToManyBase(self.db.__tables__[self.tablename])
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
    """
        Metamodel that initializes the database table model as creation of model class
    """
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return super(MetaModel, mcs).__new__(mcs, name, bases, attrs)

        # create a model with given parameters
        cls = super(MetaModel, mcs).__new__(mcs, name, bases, attrs)
        
        # if model don not have a table name set it's table name | check out wtf was db_table
        if 'Meta' not in attrs.keys() or not hasattr(attrs['Meta'], '__tablename__'):
            setattr(cls, '__tablename__', name.lower())
        else:
            setattr(cls, '__tablename__', attrs['Meta'].__tablename__)
        
        # if driver is defined book the model instace to tables dict with it's tabelename
        if hasattr(cls, '__databases__'): # needs to be changed
            databases = getattr(cls, '__databases__')
            databases[0].__tables__[cls.__tablename__] = cls
            
        
        fields = {}
        refed_fields = {}
        has_primary_key = False
        for field_name, field in cls.__dict__.items():
            if isinstance(field, ForeignKeyReverse) or isinstance(field, ManyToMany):
                field.update_attr(field_name, cls.__tablename__, cls.__databases__[0])
                refed_fields[field_name] = field
            if isinstance(field, Field):
                field.name = field_name
                fields[field_name] = field
                if isinstance(field, PrimaryKey):
                    has_primary_key = True
        # todo
        if not has_primary_key:
            pk = PrimaryKey()
            pk.name = 'id'
            fields['id'] = pk

        setattr(cls, '__fields__', fields)
        setattr(cls, '__refed_fields__', refed_fields)
        return cls

class Model(metaclass=MetaModel):
    """Base model"""
    __metaclass__ = MetaModel

    def __init__(self, **kwargs):
        for name, field in kwargs.items():
            if name not in self.__fields__.keys():
                raise DatabaseException('Unknown column: {0}, expected {1}.'.format(name, self.__fields__.keys()))
            setattr(self, name, field)

        super(Model, self).__init__()
        
    @classmethod
    def get(cls, **kwargs):
        return SelectQuery(cls).where(**kwargs).first()

    @classmethod
    def select(cls, *args):
        return SelectQuery(cls, *args)

    #@classmethod
    def update(self, *args, **kwargs):
        return UpdateQuery(self, *args, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        return DeleteQuery(cls, *args, **kwargs)

        
    def __str__(self):
        return str(vars(self))
    
    def __repr__(self):
        return str(vars(self))

    def _insert(self, db, sql):
        try:
            cursor = db.execute(sql=sql)
            if isinstance(cursor, str):
                print("Could not add to the {}. {}".format(db.database, cursor))
            else:
                self.id = cursor.lastrowid
        except OperationalError as ox:
            print("Table not found in "+db.database)
        finally:
            db.commit()

        for name, field in self.__refed_fields__.items():
            if isinstance(field, ForeignKeyReverse) or isinstance(field, ManyToManyBase):
                field.instance_id = self.id

    def save(self, databases=None):
        base_query = 'insert into {tablename}({columns}) values({items});'
        columns = []
        values = []

        for field_name, field_model in self.__fields__.items():    
            if hasattr(self, field_name) and not isinstance(getattr(self, field_name), Field):
                values.append(field_model.sql_format(getattr(self, field_name)))
                columns.append(field_name)
              
        sql = base_query.format(
            tablename=self.__tablename__,
            columns=', '.join(columns),
            items=', '.join(values)
        )
        # print(sql)
        if not databases:
            databases = self.__databases__
        
        for db in databases:
            self._insert(db, sql)
