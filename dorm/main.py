"""
    DORM Management app
"""

from contextlib import ExitStack

class DORM(object):
    """ DORM Management app """

    database_stack = ExitStack()
    model_list = list()

    def __init__(self, config):
        self.config = config

    def initialize(self):
        """ initialize all databases  """
        pass

    def discover(self):
        """ Discover the databases and order by speed """
        databases = self.config.DATABASES
        for database_type in databases:
            try:
                if database_type is 'sqlite':
                    from dorm.database.drivers.sqlite import Sqlite
                    self._add_to_stack(databases[database_type], Sqlite)
                elif database_type is 'postgres':
                    from dorm.database.drivers.postgres import Postgres
                    self._add_to_stack(databases[database_type], Postgres)
                elif database_type is 'mysql':
                    from dorm.database.drivers.mysql import Mysql
                    self._add_to_stack(databases[database_type], Mysql)
            except Exception as e:
                print("Database is not available")
                print(e)
                continue
                
    def _add_to_stack(self, parameter_list, driver):
        for params in parameter_list:
            self.database_stack.enter_context(driver(params))
            print("Added : "+ str(params))

    def check_local_databases(self):
        pass

    def migrate(self):
        """ Write changes to databases """
        pass

    def register_model(self, *args):
        self.model_list += list(args)

    def generate_models(self):
        """ Generate models from databases """
        pass

if __name__ == "__main__":
    from dorm.database.drivers.sqlite import Sqlite

    ms = Sqlite({'name':'emp', 'database_name':'datastore/employees_sqlite.db'})

    ms.discover()