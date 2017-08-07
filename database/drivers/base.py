""" doc """

from ..models import Model, ManyToMany
from utils.serializers import ModelSerializer


class BaseDriver(object):
    def __init__(self, conn):
        super(BaseDriver, self).__init__()
        self.conn = conn
        self.__tables__ = {}
        setattr(self, 'Model', Model)
        if not hasattr(self.Model, "__dbs__"):
            setattr(self.Model, '__dbs__', [])

        self.Model.__dbs__.append(self)
        # print(self.database)

    def create_table(self, model):
        tablename = model.__tablename__
        # Bug in here, foreign key does not work properly
        create_sql = ', '.join(field.create_sql()
                               for field in model.__fields__.values())
        try:
            self.execute('create table if not exists {0} ({1});'.format(
                tablename, create_sql), commit=True)
        except Exception as e:
            print(e, create_sql)

        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refered_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()

    def drop_table(self, model):
        tablename = model.__tablename__
        self.execute('drop table IF EXISTS {0};'.format(
            tablename), commit=True)
        #del self.__tables__[tablename]

        for name, field in model.__refered_fields__.items():
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
        # print("Closing")
        pass

    def generate(self, path="generated_models/", node_name="models", save=True):
        """ Generates model class code from model structre 


        """

        class_str = """class {name}(models.Model):\n"""
        field_str = """    {name} = models.{field}({extras})"""
        code = "from database import models\n\n"
        models = []
        for model_structure in self.discover():

            model = class_str.format(
                name=model_structure['table_name'].title())

            fields = []
            for column in model_structure['columns']:
                if column['extras']['fk']:
                    del column['extras']['fk']
                    del column['extras']['pk']
                    del column['extras']['not_null']
                    if column['extras']['related_field'] == 'id':
                        del column['extras']['related_field']
                    related_table = column['extras'].pop('related_table')
                    if column['extras']:
                        field = field_str.format(
                            name=column['name'], field='ForeignKey', extras=related_table.capitalize() + ', {}')
                    else:
                        field = field_str.format(
                            name=column['name'], field='ForeignKey', extras=related_table.capitalize())

                elif column['extras']['pk']:
                    del column['extras']['pk']
                    del column['extras']['fk']
                    del column['extras']['not_null']

                    if column['extras']:
                        field = field_str.format(
                            name=column['name'], field='PrimaryKey', extras=str(column['extras']))
                    else:
                        field = field_str.format(
                            name=column['name'], field='PrimaryKey', extras='')

                    fields.insert(0, field)
                    continue
                else:
                    del column['extras']['pk']
                    del column['extras']['fk']
                    field = field_str.format(name=column['name'],
                                             field=column['type'].capitalize(
                    ),  # extras=", ".join(k+"="+str(v) for k, v in column['extras'].items())
                        extras='{}')

                fields.append(field.format(str(column['extras'] or '')))
            # define primary key first, looks ugly

            # fields.insert(0, fields.pop(fields.index(next(filter(lambda x: "pk=True" in x, fields)))))
            model += "\n".join(fields) + "\n\n"

            models.append(model)
        code += "\n".join(models)
        # find current dir
        open(path + node_name + ".py", 'w').write(code)
        return models

    def execute(self, sql, commit=False):
        cursor = self.conn.cursor()
        print(sql)
        try:

            cursor.execute(sql)

            if commit:
                self.commit()

            return cursor
        except Exception as e:
            print(vars(e))
            # return e.args[0]
