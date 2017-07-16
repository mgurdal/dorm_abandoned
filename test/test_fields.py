import unittest
from unittest import mock
from dorm.database import models
from dorm.database import queries
from dorm.database.drivers.base import BaseDriver


class FieldTestCase(unittest.TestCase):
    """Base field object"""

    def setUp(self):
        self.test_field = models.Field('COLUMN_TYPE')

    def test_create_sql(self):
        """Return sql statement for create table."""

        self.test_field.name = 'COLUMN_NAME'

        self.assertEqual("COLUMN_NAME COLUMN_TYPE",
                         self.test_field.create_sql())

    def test__serialize_data(self):
        self.assertEqual(b'test', self.test_field._serialize_data('test'))


class IntegerTestCase(unittest.TestCase):
    """SQLite Integer fie"COLUMN_NAME COLUMN_TYPE"ld"""

    def setUp(self):
        self.test_int_field = models.Integer()

    def test_column_type(self):
        self.assertEqual('INTEGER', self.test_int_field.column_type)

    def test_sql_format(self):
        """sql query format of data"""
        self.assertIsInstance(self.test_int_field.sql_format(20), str)

    def test__serialize_data(self):
        self.assertEqual(self.test_int_field._serialize_data(20), 20)


class FloatTestCase(unittest.TestCase):
    """SQLite Float field"""

    def setUp(self):
        self.test_int_field = models.Float()

    def test_column_type(self):
        self.assertEqual('DOUBLE', self.test_int_field.column_type)

    def test_sql_format(self):
        """sql query format of data"""
        self.assertIsInstance(self.test_int_field.sql_format(20.6), str)

    def test__serialize_data(self):
        self.assertIsInstance(self.test_int_field._serialize_data(20.5), float)
        self.assertEqual(self.test_int_field._serialize_data(20.5), 20.5)


class CharTestCase(unittest.TestCase):
    """SQLite Char field"""

    def setUp(self):
        self.test_char_field = models.Char(max_length=4)

    def test_create_sql(self):
        self.test_char_field.name = 'test'
        self.assertEqual('"test" CHAR(4)', self.test_char_field.create_sql())

    def test_sql_format(self):
        self.assertEqual("'test'", self.test_char_field.sql_format("test"))

    def test_char_max_length_cannot_be_exceeded(self):
        try:
            self.test_char_field.sql_format("test_ex")
        except Exception as e:
            self.assertEqual('maximum length exceeded', e.args[0])


class VarcharTestCase(unittest.TestCase):
    """SQLite Varchar field"""

    def setUp(self):
        self.test_char_field = models.Varchar(max_length=4)

    def test_create_sql(self):
        self.test_char_field.name = 'test'
        self.assertEqual('"test" VARCHAR(4)',
                         self.test_char_field.create_sql())

    def test_sql_format(self):
        self.assertEqual("'test'", self.test_char_field.sql_format("test"))

    def test_char_max_length_cannot_be_exceeded(self):
        try:
            self.test_char_field.sql_format("test_ex")
        except Exception as e:
            self.assertEqual('maximum length exceeded', e.args[0])


class TextTestCase(unittest.TestCase):
    """SQLite Text field"""

    def test_sql_format(self):
        """sql query format of data"""
        self.assertEqual("'test'", models.Text().sql_format('test'))


class DateTimeTestCase(unittest.TestCase):

    def setUp(self):
        self.test_datetime = models.DateTime()

    def test_sql_format(self):
        """sql query format of data"""
        from datetime import datetime
        self.assertEqual("'2017-07-07 00:00:00'",
                         self.test_datetime.sql_format(datetime(2017, 7, 7, 0, 0, 0)))

    def test__serialize_data(self):
        from datetime import datetime
        self.assertEqual('2017-07-07 00:00:00',
                         self.test_datetime._serialize_data(datetime(2017, 7, 7, 0, 0, 0)))


class DateTestCase(unittest.TestCase):
    def setUp(self):
        self.test_date = models.Date()

    def test_sql_format(self):
        """sql query format of data"""
        from datetime import date
        self.assertEqual(
            "'2017-07-07'", self.test_date.sql_format(date(2017, 7, 7)))

    def test__serialize_data(self):
        from datetime import date
        self.assertEqual(
            '2017-07-07', self.test_date._serialize_data(date(2017, 7, 7)))


class TimestampTestCase(unittest.TestCase):

    def setUp(self):
        self.test_timestamp = models.DateTime()

    def test_sql_format(self):
        """sql query format of data"""
        from datetime import datetime
        self.assertEqual("'2017-07-07 00:00:00'",
                         self.test_timestamp.sql_format(datetime(2017, 7, 7, 0, 0, 0)))

    def test__serialize_data(self):
        from datetime import datetime
        self.assertEqual('2017-07-07 00:00:00',
                         self.test_timestamp._serialize_data(datetime(2017, 7, 7, 0, 0, 0)))


class PrimaryKeyTestCase(unittest.TestCase):

    def test_create_sql(self):
        test_pk = models.PrimaryKey()
        test_pk.name = 'test'  # models sets it
        self.assertEqual('test INTEGER NOT NULL PRIMARY KEY',
                         test_pk.create_sql())


class ForeignKeyTestCase(unittest.TestCase):

    def setUp(self):
        self.to_table = models.Model()
        self.to_table.__tablename__ = 'test_table'
        self.to_table.id = 1
        self.test_fk = models.ForeignKey(self.to_table)
        self.test_fk.name = 'test_fk'

    def test_create_sql(self):
        self.assertEqual(
            'test_fk INTEGER NOT NULL REFERENCES "test_table" ("id")', self.test_fk.create_sql())

    def test_sql_format(self):
        """sql query format of data"""
        self.assertEqual("'1'", self.test_fk.sql_format(self.to_table))

    def test__serialize_data(self):
        """ will be tested after coding is done """
        pass


class MockSQLDriver(BaseDriver):
    """Mysql Driver"""

    def __init__(self, conf):
        self.database = conf['database_name']
        conn = mock.MagicMock()
        self.conf = conf
        super(MockSQLDriver, self).__init__(conn)


class ForeignKeyReverseTestCase(unittest.TestCase):

    def setUp(self):
        self.to_table = models.Model()
        self.to_table.__tablename__ = 'test_to_table'
        self.to_table.id = 1

        self.from_table = models.Model()
        self.from_table.__tablename__ = 'test_from_table'
        self.from_table.id = 2

        self.from_table_new = models.Model()
        self.from_table_new.__tablename__ = 'test_from_table_new'
        self.from_table_new.id = 3

        self.from_table.fk_field = models.ForeignKey(self.to_table)
        self.from_table.fk_field.to_table = 'test_from_table_new'

        conf = {'host': 'test_host', 'port': 0, 'user': 'test_user',
                'passwd': 'test_password', 'database_name': 'test_database_name'}
        self.test_db = MockSQLDriver(conf)
        self.test_db.__tables__['test_from_table'] = self.from_table
        self.test_db.__tables__['test_from_table_new'] = self.from_table_new

        self.fk_reverse = models.ForeignKeyReverse('test_from_table')
        self.fk_reverse.name = None
        self.fk_reverse.tablename = None
        self.fk_reverse.instance_id = None
        self.fk_reverse.db = None
        self.fk_reverse.from_model = None
        self.fk_reverse.relate_column = None

    def test_update_attr(self):
        # sqlite.connect().cursor().fetchall.return_value = ['John', 'Bob']

        self.fk_reverse.update_attr(
            'test_name', 'test_from_table_new', self.test_db)
        self.assertEqual('test_name', self.fk_reverse.name)
        self.assertEqual('test_from_table_new', self.fk_reverse.tablename)
        self.assertIsNotNone(self.fk_reverse.db)
        self.assertIsInstance(self.fk_reverse.from_model, models.Model)
        self.assertEqual('fk_field', self.fk_reverse.relate_column)

    def test__query_sql(self):
        self.fk_reverse.from_model = models.Model()
        self.fk_reverse.relate_column = 'fk_field'
        self.fk_reverse.instance_id = 3
        qsql = self.fk_reverse._query_sql()
        self.assertIsInstance(qsql, queries.SelectQuery)
        self.assertEqual(
            'select {columns} from {tablename} where fk_field="3";', qsql.base_sql)

    def test_all_method(self):
        import types

        self.fk_reverse.from_model = models.Model()
        self.fk_reverse.relate_column = 'fk_field'
        self.fk_reverse.instance_id = 3
        qsql = self.fk_reverse._query_sql()
        
        fake_queryset = (models.Model() for _ in range(2))
        qsql.all = mock.MagicMock(return_value=fake_queryset)

        self.fk_reverse._query_sql = lambda: qsql
        self.assertIsInstance(self.fk_reverse.all(), types.GeneratorType)
        self.assertIsInstance(next(self.fk_reverse.all()), models.Model)

    def test_count_method(self):
        import types

        self.fk_reverse.from_model = models.Model()
        self.fk_reverse.relate_column = 'fk_field'
        self.fk_reverse.instance_id = 3
        qsql = self.fk_reverse._query_sql()
        
        fake_queryset = (models.Model() for _ in range(2))
        qsql.all = mock.MagicMock(return_value=fake_queryset)

        self.fk_reverse._query_sql = lambda: qsql
        self.assertIsInstance(self.fk_reverse.all(), types.GeneratorType)
        self.assertEqual(len(list(self.fk_reverse.all())), 2)


class ManyToManyBaseTestCase(unittest.TestCase):

    def test_update_attr(self):
        pass

    def test_add(self):
        pass

    def test_remove(self):
        pass

    def test_all(self):
        pass

    def test_count(self):
        pass

    def test__query_sql(self):
        pass


class ManyToManyTestCase(unittest.TestCase):

    def test_update_attr(self):
        pass

    def test_create_m2m_table(self):
        pass

    def test_drop_m2m_table(self):
        pass

    def test_create_reversed_field(self):
        pass

    def test_delete_reversed_field(self):
        pass


if __name__ == '__main__':
    unittest.main()
