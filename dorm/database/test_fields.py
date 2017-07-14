import unittest
import queries, models


class FieldTestCase(unittest.TestCase):
    """Base field object"""

    def test_create_sql(self):
        """Return sql statement for create table."""
        pass

class IntegerTestCase(unittest.TestCase):
    """SQLite Integer field"""

    def test_sql_format(self, data):
        """sql query format of data"""
        pass
    
    def test__serialize_data(self, data):
        pass

class FloatTestCase(unittest.TestCase):
    """SQLite Float field"""
    def test_sql_format(self, data):
        """sql query format of data"""
        pass
    
    def test__serialize_data(self, data):
        pass

class CharTestCase(unittest.TestCase):
    """SQLite Char field"""

    def test_create_sql(self):
        pass

    def test_sql_format(self, data):
        """sql query format of data"""
        pass
        
    def test__serialize_data(self, data):
        pass

class VarcharTestCase(unittest.TestCase):
    """SQLite Varchar field"""

    def test_create_sql(self):
        pass

    def test_sql_format(self, data):
        """sql query format of data"""
        pass

class TextTestCase(unittest.TestCase):
    """SQLite Text field"""

    def test_sql_format(self, data):
        """sql query format of data"""
        pass

class DateTimeTestCase(unittest.TestCase):

    def test_sql_format(self, data):
        pass
    
    def test__serialize_data(self, data):
        pass
    def test_to_string(self, data, format='%Y-%m-%d %H:%M:%S'):
        pass

class DateTestCase(unittest.TestCase):
    def test___init__(self):
        pass

    def test_sql_format(self, data):
        pass
    
    def test__serialize_data(self, data):
        pass
    def test_to_string(self, data, format='%Y-%m-%d'):
        pass

class TimestampTestCase(unittest.TestCase):

    def test_sql_format(self, data):
        pass
    
    def test__serialize_data(self, data):
        pass

    def test_to_string(self, data, format='%Y-%m-%d %H:%M:%S'):
        pass


class PrimaryKeyTestCase(unittest.TestCase):

    def test_create_sql(self):
        pass

class ForeignKeyTestCase(unittest.TestCase):

    def test_create_sql(self):
        pass

    def test_sql_format(self, data):
        """sql query format of data"""
        pass  

    def test__serialize_data(self, data):
        pass
    
class ForeignKeyReverseTestCase(unittest.TestCase):

    def test_update_attr(self, name, tablename, db):
        pass

    def test_all(self):
        pass

    def test_count(self):
        pass

    def test__query_sql(self):
        pass

class TestCaseTestCase(unittest.TestCase):

    def test_update_attr(self, name, tablename, db):
        pass

    def test_add(self, to_instance):
        pass

    def test_remove(self, to_instance):
        pass

    def test_all(self):
        pass

    def test_count(self):
        pass

    def test__query_sql(self):
        pass

class ManyToManyTestCase(unittest.TestCase):

    def test_update_attr(self, name, tablename, db):
        pass

    def test_create_m2m_table(self):
        pass

    def test_drop_m2m_table(self):
        pass

    def test_create_reversed_field(self):
        pass

    def test_delete_reversed_field(self):
        pass
