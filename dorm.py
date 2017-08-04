from database import models
from database.drivers.sqlite import Sqlite
from config import MAIN_NODE, NODES
from pprint import pprint

class Node(models.Model):
    __tablename__ = "node"
    _id = models.PrimaryKey()
    server_ip = models.IP()
    port = models.Integer()
    database_name = models.Char()
    user = models.Char()
    password = models.Char()
    db_type = models.Char()
    #tables = models.ManyToMany(models.Model)
    # driver = models.DriverField() # implement it pls


class DORM(object):
    """ DORM is an ORM interface that manages 'Nodes' which manges the database tables via Models"""
    db = Sqlite({'database_name':'node.db'})
    def from_dict(self, config_list):
        """ Generates Nodes from config file """
        nodes = [Node(**conf) for conf in config_list]
        setattr(self, 'nodes', nodes)


    def discover(self):
        """ Discovers the tables inside nodes """
        for i, node in enumerate(self.nodes):

            if node.db_type == 'sqlite':
                # solution 1
                # node.__databases__.append(Sqlite(vars(node)))

                
                sq = Sqlite(vars(node))
                    
                sq.create_table(node)
                node.save(sq)
                #print(list(node.select('_id', target_databases=[sq]).all()))
                #print("-"*10+"Node"+"-"*10)
                #pprint(vars(sq))
                #print("-"*20)
                #sq.create_table(node)
                #tables = sq.discover()
                #print("-"*10+"Tables"+"-"*10)
                #pprint(tables)
                #print("-"*20)
                #node.node_num = 'node_'+str(id(node))
                
                codes = sq.generate("generated_models/")
                for m in codes:
                    exec(m)
                #from generated_models import models

                """ 
                Generate models using metaclass feature
                (I am not smart enough, yet)
                for table in tables:
                    # generate model from table
                    model = type(table['table_name'].capitalize(),
                                 (models.Model,), {})
                    model.__tablename__ = table['table_name']
                    node.__tablename__ = 'node'
                    sq.__tables__[table['table_name']] = model
                    # make (manytomany if posible) relationship between model and node
                    #print("Model", vars(model))
                    # not working yet
                    #sq.create_table(model)
                    rel = models.ManyToMany(model)
                    rel.update_attr(node.node_num, node.node_num, sq) 
                """
                

if __name__ == "__main__":

    d = DORM()
    d.from_dict(NODES)
    c = d.discover()



"""
class DORM(models.Model):


class Driver(models.Model):
    server_ip = models.IP() # pingable
    database_ip = models.IP()
    port = models.Port()
    database_type = models.Char()
    database_name = models.Char()
    user = models.Char()
    password = models.Password()

class Model(models.Model):
    id = models.PrimaryKey()
    driver = models.ForeignKey(Driver)
    


qs = dorm.drivers.all()
[driver, driver, ...]
[model, model, ...]

d = Driver(conf)
m = Model(id=1, driver=d)


models
{id=1: driver_id:1}
"""
