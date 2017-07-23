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
        self.assertEqual('test CHAR(4)', self.test_char_field.create_sql())

    def test_sql_format(self):
        self.assertEqual("'test'", self.test_char_field.sql_format("test"))

    def test_char_max_length_cannot_be_exceeded(self):
        try:
            self.test_char_field.sql_format("test_ex")
        except Exception as e:
            self.assertEqual('maximum length exceeded', e.args[0])


class VarCharTestCase(unittest.TestCase):
    """SQLite VarChar field"""

    def setUp(self):
        self.test_char_field = models.VarChar(max_length=4)

    def test_create_sql(self):
        self.test_char_field.name = 'test'
        self.assertEqual('test VARCHAR(4)',
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
            'test_fk INTEGER NOT NULL REFERENCES test_table (id)', self.test_fk.create_sql())

    def test_sql_format(self):
        """sql query format of data"""
        self.assertEqual("1", self.test_fk.sql_format(self.to_table))

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

        self.from_table = models.Model()
        self.from_table.__tablename__ = 'test_table'
        self.from_table.test_table = models.ForeignKey(
            self.from_table.__tablename__)
        self.db = MockSQLDriver({'database_name': 'test'})
        self.db.__tables__['test_table'] = self.from_table
        models.Model.__databases__ = [self.db]
        models.Model.__tablename__ = 'test_table'
        self.fk_reverse = models.ForeignKeyReverse(self.from_table)

    def test_update_attr(self):
        fk_reverse = self.fk_reverse
        db = self.db
        fk_reverse.update_attr('test', self.from_table, db)
        self.assertIsNotNone(fk_reverse.name)
        self.assertIsNotNone(fk_reverse.tablename)
        self.assertIsNotNone(fk_reverse.db)
        self.assertEqual(fk_reverse.relate_column, "test_table")

    def test__query_sql(self):
        db = self.db
        fk_reverse = self.fk_reverse
        fk_reverse.update_attr('test', self.from_table, db)
        self.assertIsInstance(fk_reverse._query_sql(), queries.SelectQuery)

    # testi :(
    def test_all_method(self):
        import types
        db = self.db
        fk_reverse = self.fk_reverse
        fk_reverse.update_attr('test', self.from_table, db)
        res = self.fk_reverse._query_sql().all()
        self.assertIsInstance(res, types.GeneratorType)

    def test_count_method(self):
        db = self.db
        fk_reverse = self.fk_reverse
        fk_reverse.update_attr('test', self.from_table, db)
        # fake count function
        queries.SelectQuery.count = lambda _: ([0] for _ in range(1))
        res = next(self.fk_reverse._query_sql().count())
        self.assertIsInstance(res, list)
        self.assertEquals(res, [0])


class ManyToManyBaseTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_update_attr(self):
        pass

    def test__query_sql(self):
        pass

    def test_add(self):
        pass

    def test_remove(self):
        pass

    def test_all(self):
        pass

    def test_count(self):
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
