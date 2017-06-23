"""
    DORM Management app
"""

from .database.drivers.sqlite import Sqlite
from .database.drivers.postgres import Postgres

from contextlib import ExitStack

 # sudo docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

class DORM(object):
    """ DORM Management app """

    database_stack = ExitStack()

    def __init__(self, config):
        self.config = config

    def initialize(self):
        """ initialize all databases  """
        pass

    def discover(self):
        """ Discover the databases and order by speed """
        databases = self.config.DATABASES

        for database_type in databases:
            if database_type is 'sqlite':
                self._add_to_stack(databases[database_type], Sqlite)
            elif database_type is 'postgres':
                self._add_to_stack(databases[database_type], Postgres)

    def _add_to_stack(self, parameter_list, driver):
        for params in parameter_list:
            self.database_stack.enter_context(driver(params))

    def check_local_databases(self):
        pass

    def migrate(self):
        """ Write changes to databases """
        pass

    def generate_models(self):
        """ Generate models from databases """
        pass
