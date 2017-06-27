"""SQLite Drivers"""
import sys
import sqlite3
import threading
from pprint import pprint
#from .base import BaseDriver
from ..models import Model, ManyToMany

class Sqlite(threading.local):
    def __init__(self, conf):
        self.database = conf['database_name']
        self.conn = sqlite3.connect(database=self.database,
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
                                   )
        self.conf = conf
        self.__tables__ = {}
        setattr(self, 'Model', Model)
        if not hasattr(self.Model, "__dbs__"):
            setattr(self.Model, '__dbs__', [])

        self.Model.__dbs__.append(self)

    def create_table(self, model):
        tablename = model.__tablename__
        # Bug in here, foreign key does not work properly
        create_sql = ', '.join(field.create_sql() for field in model.__fields__.values())
        try:
            self.execute('create table {0} ({1});'.format(tablename, create_sql), commit=True)
        except Exception as e:
            print(e)

        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()

    def drop_table(self, model):
        tablename = model.__tablename__
        self.execute('drop table IF EXISTS {0};'.format(tablename), commit=True)
        #del self.models.__tables__[tablename]

        for name, field in model.__refed_fields__.items():
            if isinstance(field, ManyToMany):
                field.drop_m2m_table()

    def discover(self):
        """ Creates model structure from database tables """

        table_list = []
        q = "SELECT sql FROM sqlite_master;"
        tables = self.execute(q).fetchall()
        for table in tables:
            t = table[0].replace("CREATE TABLE ", "")
            table_name = t[:t.find(" ")]
            columns = t[t.find(" "):].strip()[1:-1].split(", ")
            table_list.append({table_name:columns})

        return table_list

    def generate(self, save=True):
        """ Generates model class code from model structre """

        class_str = """class {}(models.Model):\n"""
        field_str = """    {} = models.{}({})\n"""
        code = ""
        for model_structure in self.discover():
            
            model=""
            for key, val in model_structure.items():
                
                model = class_str.format(key.title())
                for column in val:
                    extra = []
                    column = column.lower()
                    #extra.append("null=False")
                    #extra.append("unique=False")

                    field_name, field_type, *_ = column.split(" ")
                    if "(" in field_type:
                        extra.append("max_length="+field_type[field_type.find("(")+1:field_type.find(")")])
                        field_type = field_type[:field_type.find("(")]
                    if "primary key" in column:
                        model += field_str.format(field_name, "PrimaryKey", ", ".join(extra))
                    elif "references" in column:
                        target_table = column[:column.find("REFERENCES ")].split(" (")[0].split(" ")[0]
                        extra.append(target_table.title())
                        model += field_str.format(field_name, "ForeignKey", ", ".join(extra))
                    else:
                        model += field_str.format(field_name, field_type.title(), ", ".join(extra))
            code += model
        
        if save:
            with open("models/"+self.conf['name'], 'w') as f:
                f.write("from dorm.database import models\n\n")
                f.write(code)
        return code

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def execute(self, sql, commit=False):
        cursor = self.conn.cursor()

        try:
            #pprint(sql)
            cursor.execute(sql)

            if commit:
                self.commit()
            #pprint(sql)
            return cursor
        except Exception as e:
            raise e

class SqliteNotDoneYet(object):
    """SQLite Driver"""
    def __init__(self, conf):
        super(Sqlite, self).__init__(adapter=sqlite3,
                                     database=conf['database_name'],
                                     detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
