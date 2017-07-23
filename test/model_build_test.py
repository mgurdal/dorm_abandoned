""" code generation tests """
import os
import unittest
from dorm.database.drivers.sqlite import Sqlite
from dorm.database.models import Model, Integer


class Testmodel(Model):
    test_int = Integer()


class SqliteModelBuildTestCase(unittest.TestCase):
    """ Check if the model codes generates corretly from databases """

    def setUp(self):
        self.database = Sqlite(
            {"database_name": "test.db", "name": "test_model"})

        self.database.create_table(Testmodel)

    def test_table_structre_generated_from_database(self):
        """ test model name and fields fetched corretly from database"""

        discovered_models = self.database.discover()
        self.assertEquals(1, len(discovered_models))

        model_structure = discovered_models[0]
        self.assertIn('testmodel', model_structure.keys())

        setattr(self, 'model_structure', model_structure)

        fields = model_structure['testmodel']
        self.assertEquals(2, len(fields))

    def test_code_generated_from_table_structre(self):
        """ test model name and fields generated corretly from model structure"""

        test_code = """from dorm.database import models\n\nclass Testmodel(models.Model):\n    id = models.PrimaryKey()\n    test_int = models.Integer()\n\n"""
        generated_code = self.database.generate(save=True)
        self.assertEquals(test_code, generated_code)

    def tearDown(self):
        os.remove('test.db')
        self.database.close()
        del self.database


if __name__ == "__main__":
    unittest.main()
