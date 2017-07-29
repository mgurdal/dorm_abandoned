import psycopg2
from .base import BaseDriver

class Postgres(BaseDriver):
    """Postgres Driver"""
    def __init__(self, conf):
        conn = psycopg2.connect(dbname=conf['database_name'],
                                user=conf['user'],
                                password=conf['password'],
                                host=conf['host'],
                                port=conf['port']
                               )
        super(Postgres, self).__init__(conn, conf)
