""" code generation tests """

import unittest
from dorm.database.drivers.sqlite import Sqlite
from dorm.database import models

class SqliteModelBuildTestCase(unittest.TestCase):
    """ Check if the model codes generates corretly from databases """
    def setUp(self):
        self.database = Sqlite({"database_name":"test1.db", "name":"test_model.py"})
        self.database 
        class Testmodel(models.Model):
            test_int = models.Integer()
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

        test_code = """class Testmodel(models.Model):\n    id = models.PrimaryKey()\n    test_int = models.Integer()\n"""
        generated_code = self.database.generate(save=True)
        self.assertEquals(test_code, generated_code)

    def tearDown(self):
        self.database.close()

if __name__ == "__main__":
    unittest.main()