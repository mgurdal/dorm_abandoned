
"""
Bunch of field classes that represents the database data types and relations
"""

class DatabaseException(Exception):
    pass

class Field(object):
    """
    Base field
    """
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None

    def create_sql(self):
        """Return sql statement for create table."""
        return '"{0}" {1}'.format(self.name, self.column_type)


class IntegerField(Field):
    """
    
    """
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
