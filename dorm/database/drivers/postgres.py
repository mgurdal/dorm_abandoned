import psycopg2
from .base import BaseDriver

class Postgres(BaseDriver):
    """Postgres Driver"""
    def __init__(self, **kwargs):
        print(kwargs)
        super(Postgres, self).__init__(adapter=psycopg2,
                                       database=kwargs['database'],
                                       user=kwargs['user'],
                                       password=kwargs['password'],
                                       port=kwargs['port'])
