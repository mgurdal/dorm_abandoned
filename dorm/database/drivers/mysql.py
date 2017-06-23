import MySQLdb
from .base import BaseDriver

class Mysql(BaseDriver):
    """Mysql Driver"""
    def __init__(self, conf):
        self.database = conf['database_name']
        conn = MySQLdb.connect(host=conf['host'],
                               port=conf['port'], user=conf['user'],
                               passwd=conf['password'],
                               db=conf['database_name']
                              )
                              
        super(Mysql, self).__init__(conn)
