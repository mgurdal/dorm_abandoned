import unittest
from dorm.database import models

class FieldTestCase(unittest.TestCase):
    """Base field object"""

    def test_create_sql(self):
        """Return sql statement for create table."""
        test_field = models.Field('COLUMN_TYPE')
        test_field.name = 'COLUMN_NAME'

        self.assertEqual("COLUMN_NAME COLUMN_TYPE", test_field.create_sql())

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

    def test_create_sql(self):
        pass

    def test_sql_format(self):
        """sql query format of data"""
        pass
        
    def test__serialize_data(self):
        pass

class VarcharTestCase(unittest.TestCase):
    """SQLite Varchar field"""

    def test_create_sql(self):
        pass

    def test_sql_format(self):
        """sql query format of data"""
        pass

class TextTestCase(unittest.TestCase):
    """SQLite Text field"""

    def test_sql_format(self):
        """sql query format of data"""
        pass

class DateTimeTestCase(unittest.TestCase):

    def test_sql_format(self):
        pass
    
    def test__serialize_data(self):
        pass
    def test_to_string(self):
        pass

class DateTestCase(unittest.TestCase):
    def test___init__(self):
        pass

    def test_sql_format(self):
        pass
    
    def test__serialize_data(self):
        pass
    def test_to_string(self):
        pass

class TimestampTestCase(unittest.TestCase):

    def test_sql_format(self):
        pass
    
    def test__serialize_data(self):
        pass

    def test_to_string(self):
        pass


class PrimaryKeyTestCase(unittest.TestCase):

    def test_create_sql(self):
        pass

class ForeignKeyTestCase(unittest.TestCase):

    def test_create_sql(self):
        pass

    def test_sql_format(self):
        """sql query format of data"""
        pass  

    def test__serialize_data(self):
        pass
    
class ForeignKeyReverseTestCase(unittest.TestCase):

    def test_update_attr(self):
        pass

    def test_all(self):
        pass

    def test_count(self):
        pass

    def test__query_sql(self):
        pass

class TestCaseTestCase(unittest.TestCase):

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