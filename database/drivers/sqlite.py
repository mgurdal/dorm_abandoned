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
                    field_parser.named['extras'] = {}
                    field_parser.named['extras']['pk'] = False
                    field_parser.named['extras']['fk'] = False
                    # if column does not have argument. e.g CHAR(15)
                    if field_parser.named['type'][-1] == r")":
                        field_parser.named['extras']['size']=field_parser.named['type'][field_parser.named['type'].rfind("(")+1:-1]
                        field_parser.named['type'] = field_parser.named['type'][:field_parser.named['type'].rfind("(")]
                    if 'rest' in field_parser.named.keys():
                        if 'NOT NULL' in field_parser.named['rest']:
                            field_parser.named['extras']['not_null'] = True

                        if 'PRIMARY KEY' in field:
                            field_parser.named['extras']['pk'] = True

                        if 'REFERENCES' in field_parser.named['rest']:
                            field_parser.named['extras']['fk'] = True
                            table_str = field.split(" REFERENCES ")[1]
                            related_table = parse(
                                "{related_table} ({related_field})", table_str).named
                            field_parser.named['extras'].update(related_table)
                        del field_parser.named['rest']
                    columns.append(field_parser.named)

            table_parser.named['columns'] = columns
            table_list.append(table_parser.named)
        return table_list

