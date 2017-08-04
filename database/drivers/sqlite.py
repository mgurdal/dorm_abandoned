"""SQLite Drivers"""
import sys
import sqlite3
import threading
from pprint import pprint

from parse import parse

from .base import BaseDriver
from ..models import Model, ManyToMany


class Sqlite(BaseDriver):
    def __init__(self, conf):
        self.database = conf['database_name']
        self.conn = sqlite3.connect(database=self.database,
                                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
                                    )
        self.conf = conf
        self.__tables__ = {}

        # I do not wanna do this
        # instead I can reach to the database driver from
        # the models's conf variable
        # self.Model.__conf__.update(self.conf) # model conf update this

    def create_table(self, model):
        tablename = model.__tablename__

        # Bug in here, foreign key does not work properly
        # print(model.__fields__.values())
        create_sql = ', '.join(field.create_sql()
                               for field in model.__fields__.values())

        try:
            self.execute('create table if not exists {0} ({1});'.format(
                tablename, create_sql), commit=True)
        except Exception as e:
            raise e

        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refered_fields__.values():
            if isinstance(field, ManyToMany):
                #print("Creating many to many", field)
                field.create_m2m_table()

    def drop_table(self, model):
        tablename = model.__tablename__
        self.execute('drop table IF EXISTS {0};'.format(
            tablename), commit=True)
        #del self.models.__tables__[tablename]

        for name, field in model.__refered_fields__.items():
            if isinstance(field, ManyToMany):
                field.drop_m2m_table()

    def discover(self):
        """ Creates model structure from database tables """

        table_list = []
        q = "SELECT sql FROM sqlite_master;"
        tables = self.execute(q).fetchall()
        for table in tables:
            if table[0] == None:
                continue

            table_parser = parse(
                'CREATE TABLE {table_name} ({columns})', table[0])
            fs = table_parser.named['columns'].split(', ')
            columns = []
            for field in fs:
                field_parser = parse('{name} {type} {rest}', field) or parse(
                    '{name} {type}', field)
                if field_parser is not None:
                    field_parser.named['pk'] = False
                    field_parser.named['fk'] = False
                    field_parser.named['is_null'] = False
                    if field_parser.named['type'][-1] != r")":
                        field_parser.named['type'] += r"()" 
                    if 'rest' in field_parser.named.keys():
                        if 'NOT NULL' in field_parser.named['rest']:
                            field_parser.named['not_null'] = True

                        if 'PRIMARY KEY' in field:
                            field_parser.named['pk'] = True

                        if 'REFERENCES' in field_parser.named['rest']:
                            field_parser.named['fk'] = True
                            table_str = field.split(" REFERENCES ")[1]
                            related_table = parse(
                                "{related_table} ({related_field})", table_str).named
                            field_parser.named['extras'] = related_table
                        del field_parser.named['rest']
                    columns.append(field_parser.named)

            table_parser.named['columns'] = columns
            table_list.append(table_parser.named)
        return table_list

    def generate(self, path="generated_models/", save=True):
        """ Generates model class code from model structre """

        class_str = """class {}(models.Model):\n"""
        field_str = """    {} = models.{}({})\n"""
        code = "from dorm.database import models\n\n"
        for model_structure in self.discover():

            model = class_str.format(model_structure['table_name'].title())
                
            #for key, val in model_structure.items():

            for column in model_structure['columns']:
                extra = []
                column = column.lower()
                # extra.append("null=False")
                # extra.append("unique=False")

                field_name, field_type, *_ = column.split(" ")
                if "(" in field_type:
                    extra.append(
                        "max_length=" + field_type[field_type.find("(") + 1:field_type.find(")")])
                    field_type = field_type[:field_type.find("(")]
                if "primary key" in column:
                    model += field_str.format(field_name,
                                              "PrimaryKey", ", ".join(extra))
                elif "references" in column:
                    try:
                        target_table = column[column.find("references"):].split(
                            " (")[0].split(" ")[1]
                        extra.append(target_table.title())
                        model += field_str.format(field_name,
                                                  "ForeignKey", ", ".join(extra))
                    except:
                        print(column)
                else:
                    model += field_str.format(field_name,
                                              field_type.title(), ", ".join(extra))
            code += model + "\n"

        if save:
            with open(path+"models" + ".py", 'w') as f:
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
            cursor.execute(sql)

            if commit:
                try:
                    print("RAN: ", sql)
                    self.commit()
                except e:
                    print(e)
            return cursor
        except Exception as e:
            # print(sql)
            raise e
            return str(e)


"""
class DORM(models.Model):


class Driver(models.Model):
    server_ip = models.IP() # pingable
    database_ip = models.IP()
    port = models.Port()
    database_type = models.Char()
    database_name = models.Char()
    user = models.Char()
    password = models.Password()

class Model(models.Model):
    id = models.PrimaryKey()
    driver = models.ForeignKey(Driver)
    


qs = dorm.drivers.all()
[driver, driver, ...]
[model, model, ...]

d = Driver(conf)
m = Model(id=1, driver=d)


models
{id=1: driver_id:1}
"""
