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
                    from .database.drivers.sqlite import Sqlite
                    self._add_to_stack(databases[database_type], Sqlite)
                elif database_type is 'postgres':
                    from .database.drivers.postgres import Postgres
                    self._add_to_stack(databases[database_type], Postgres)
                elif database_type is 'mysql':
                    from .database.drivers.mysql import Mysql
                    self._add_to_stack(databases[database_type], Mysql)
            except Exception:
                print("Database is not available")
                continue
    def _add_to_stack(self, parameter_list, driver):
        for params in parameter_list:
            self.database_stack.enter_context(driver(params))

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
