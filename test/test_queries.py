import unittest
from mock import patch, MagicMock
from dorm.database.queries import DeleteQuery


class DeleteQueryTestCase(unittest.TestCase):
    """ test delete queries in here """

    def setUp(self):
        self.stub_model = MagicMock()
        self.stub_model.__tablename__ = "stub_model"
        self.stub_model.__databases__ = []
    
    def test_delete_query_without_args_n_kwargs(self):
        dq = DeleteQuery(self.stub_model)
        self.assertEqual('delete from stub_model;', dq.sql)

    def test_delete_query_with_args_without_kwargs(self):
        dq = DeleteQuery(self.stub_model, 'id=1')
        self.assertEqual('delete from stub_model where id=1;', dq.sql)

    def test_delete_query_with_kwargs_without_args(self):
        dq = DeleteQuery(self.stub_model, id=1)
        self.assertEqual('delete from stub_model where id=1;', dq.sql)

    def test_delete_query_with_kwargs_n_args(self):
        dq = DeleteQuery(self.stub_model, 'id=1', name='test')
        self.assertEqual('delete from stub_model where id=1 and name=test;', dq.sql)
    
    @patch('dorm.database.queries.db_job_spawner')
    def test_delete_query_with_kwargs_n_args(self, job_spawner):
        dq = DeleteQuery(self.stub_model, 'id=1', name='test')
        dq.commit()
        job_spawner.assert_called_with(dq.sql, self.stub_model.__databases__, commit=True)
