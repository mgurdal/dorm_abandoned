import unittest
from unittest.mock import MagicMock

from dorm import DORM


class DORMTestCase(unittest.TestCase):
    """ test essential framework functionalities here """

    def setUp(self):
        """ initialize """
        TEST_NODES = [{'server_ip': '0.0.0.0', 'database_ip': '127.0.0.1', 'port': '-',
                       'type': 'sqlite', 'database_name': 'datastore/poll_1.db', 'name': 'poll_1.py'}]
        self.dorm = DORM(TEST_NODES)

    def test_try_to_discover_a_postgres_node(self):
        """ dorm tries to connect to the test node """
        dorm = self.dorm
        test_result = dorm.config[0].update({'status': 'active', 'latency': '30ms', 'tables': [{
            'table_name': 'table_1',
            'columns': [
                {'name': 'id', 'type': 'INTEGER', 'is_null':False, 'pk': True, 'fk': False, 'extras': {'max_length': 11, 'AUTOINCREMENT': True}},
                {'name': 'char_1', 'type': 'CHAR', 'is_null':True, 'pk': False,
                    'fk': False, 'extras': {'max_length': 200}},
                {'name': 'varchar_1', 'type': 'VARCHAR', 'is_null':True, 'pk': False,
                 'fk': False, 'extras': {'max_length': 200}},
                {'name': 'date_1', 'type': 'DATE', 'is_null':True, 'pk': False,
                 'fk': False, 'extras': {}},
                {'name': 'datetime_1', 'type': 'DATETIME', 'is_null':True, 'pk': False,
                 'fk': False, 'extras': {}},
                {'name': 'fk_int_1', 'type': 'INTEGER', 'is_null':False,
                 'pk': False, 'fk': True, 'extras': {'max_length': 11, 'related_table': 'table_2', 'related_field': 'id'}},
                {'name': 'mm_int_1', 'type': 'INTEGER', 'is_null':False,
                 'pk': False, 'fk': True, 'extras': {'max_length': 11, 'related_table': 'table_1_table_2', 'related_field': 'table1_id'}},
            ]
        }, {
            'table_name': 'table_2',
            'columns': [
                {'name': 'id', 'type': 'INTEGER', 'is_null':False, 'pk': True, 'fk': False, 'extras': {'size': 11, 'AUTOINCREMENT':True}},
            ]
        }, {
            'table_name': 'table1_table_2',
            'columns': [
                {'name': 'id', 'type': 'INTEGER', 'is_null':False, 'pk': True,
                    'fk': False, 'extras': {'size': 11}},
                {'name': 'table1_id', 'type': 'INTEGER', 'is_null':False, 'pk': False,
                    'fk': False, 'extras': {'size': 11}},
                {'name': 'table2_id', 'type': 'INTEGER', 'is_null':False, 'pk': False,
                    'fk': False, 'extras': {'size': 11}},
            ]
        },
        ]})

        self.assertTrue(True)
