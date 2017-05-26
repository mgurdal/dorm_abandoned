class MongoDB(threading.local):
    """Not done yet"""
    def __init__(self, database):
        super(MongoDB, self).__init__()
        self.database = MongoClient()[database] # create mongo database
        self.conn = self.database

        self.__tables__ = {}
        setattr(self, 'Model', Model)
        setattr(self.Model, '__db__', self)    
    
    def create_table(self, model):
        tablename = model.__tablename__
        self.database[tablename] # create collection

        # register the given model as a table to database  if  not 
        if tablename not in self.__tables__.keys():
            self.__tables__[tablename] = model
 
        """ # still do not know what I am supposed to do with relations
        for field in model.__refed_fields__.values():
            if isinstance(field, ManyToMany):
                field.create_m2m_table()
        """
        return tablename
                   
    def drop_table(self, model):
        tablename = model.__tablename__
        # test
        self.database[tablename].drop()
        del self.__tables__[tablename]


    def commit(self):
        # what to do?
        #self.conn.commit()
        pass

    def rollback(self):
        # what to do?
        #self.conn.rollback()
        pass

    def close(self):
        # what
        #self.conn.close()
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # self.close()
        print("exiting now")

    def execute(self, bson, commit=False):
            #print(sql)
            cursor.execute(sql)
            
            return cursor
