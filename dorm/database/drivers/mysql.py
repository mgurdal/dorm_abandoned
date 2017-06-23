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

    def create_table(self, model):
        tablename = model.__tablename__
        # Bug in here, foreign key does not work properly
        create_sql = ', '.join(field.create_sql().replace("\"", "") for field in model.__fields__.values())
        try:
            self.execute('create table if not exists {0} ({1});'.format(tablename, create_sql), commit=True)
        except Exception as e:
            print(e, create_sql)

        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model

        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()