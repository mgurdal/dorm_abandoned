"""
Test query objects here
"""

import unittest
import queries, models


class SelectQueryTestCase(unittest.TestCase):
    """
        Select query test for all supported databases
        cursor = MagicMock(Cursor)
        cursor.fetchall.return_value = [{'column1': 'hello', 'column2': 'world'}]
    """

    def setUp(self):
        """ init query deps """
        class DummyModel(models.Model):
            """dummy thingy"""
            dummy_field = models.Integer()


        self.test_model = DummyModel(dummy_field=1)
        self.select_query = queries.SelectQuery(self.test_model)

    def test_select_query_with_star_parameter(self):
        pass

    def tearDown(self):
        pass
