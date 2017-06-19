import psycopg2
from .base import BaseDriver

class Postgres(BaseDriver):
    """Postgres Driver"""
    def __init__(self, conf):
        super(Postgres, self).__init__(adapter=psycopg2,
                                       database=conf['database'],
                                       user=conf['user'],
                                       password=conf['password'],
                                       port=conf['port'])
