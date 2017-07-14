"""
    ADD tests to run
"""


from unittest import TestLoader, TextTestRunner, TestSuite
from test.field_test import FieldTestCase
from test.query_test import QueryTestCase
from test.model_build_test import SqliteModelBuildTestCase

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(FieldTestCase),
        loader.loadTestsFromTestCase(QueryTestCase),
        loader.loadTestsFromTestCase(SqliteModelBuildTestCase)
        ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
