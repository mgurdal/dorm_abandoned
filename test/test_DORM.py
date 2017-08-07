import unittest
from unittest.mock import MagicMock, patch

from ..dorm import DORM


class DORMTestCase(unittest.TestCase):
    """ test essential framework functionalities here """

    def setUp(self):
        """ initialize """
        self.dorm = DORM()
        self.dummy_config = [{
            'server_ip': '123.123.123.123',
            'db_type': 'sqlite',
            'database_name': 'test.db',
            'user': 'test',
            'password': 'test',
            'port': 0
        }]

    @patch('dorm.Node')
    def test_create_nodes_from_config(self, Node):
        dorm = self.dorm
        dorm.from_dict(self.dummy_config)
        self.assertTrue(hasattr(dorm, 'nodes'))

    def test_discover(self):
        dorm = self.dorm
        dorm.from_dict(self.dummy_config)
        dorm.discover()
        self.assertTrue(hasattr(dorm.nodes[0], 'tables'))
    