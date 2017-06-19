""" doc """

from ..models import Model, ManyToMany
from dorm.utils.serializers import ModelSerializer


class BaseDriver(object):
    def __init__(self, adapter=None, **kwargs):
        super(BaseDriver, self).__init__()
        self.database = kwargs['database_name']
        self.conn = adapter.connect(**kwargs)

        self.__tables__ = {}
        setattr(self, 'Model', Model)
        if not hasattr(self.Model, "__dbs__"):
            setattr(self.Model, '__dbs__', [])
        
        self.Model.__dbs__.append(self)
            #print(self.database)

    def create_table(self, model):
        tablename = model.__tablename__
        # Bug in here, foreign key does not work properly
        create_sql = ', '.join(field.create_sql() for field in model.__fields__.values())
        try:
            self.execute('create table {0} ({1});'.format(tablename, create_sql), commit=True)
        except Exception as e:

            print(e, create_sql)
        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()

    def drop_table(self, model):
        tablename = model.__tablename__
        self.execute('drop table IF EXISTS {0};'.format(tablename), commit=True)
        #del self.__tables__[tablename]

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
        #print("Closing")
        pass
    
    def execute(self, sql, commit=False):
        cursor = self.conn.cursor()
        
        try:
            print(sql)
            cursor.execute("rollback;"+sql)
            print("success")
            if commit:
                self.commit()
            return cursor
        except Exception as e:
            raise e

