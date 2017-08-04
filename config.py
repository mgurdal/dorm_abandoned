import os
import sys


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


MODEL_DIR = "/mymodels/"

CLUSTERS = [
    {'address': '127.0.0.1', 'name': 'local_cluster_1', 'port': '40001'},
    {'address': '127.0.0.1', 'name': 'local_cluster_2', 'port': '40002'},
    {'address': '127.0.0.1', 'name': 'local_cluster_3', 'port': '40003'},
    {'address': '127.0.0.1', 'name': 'local_cluster_4', 'port': '40004'},
]

MAIN_NODE = {'server_ip': '0.0.0.0', 'port': 5000,
             'db_type': 'sqlite', 'database_name': 'dorm.db', 'user': 'sky', 'password': 'test'},


NODES = [
    {'server_ip': '0.0.0.0', 'port': 0, 'db_type': 'sqlite',
        'database_name': 'datastore/generated.db', 'user': '-', 'password': '-'},
    {'server_ip': '0.0.0.0', 'port': 5432, 'db_type': 'postgres',
        'database_name': 'test', 'user': 'postgres', 'password': 'mysecretpassword'},
    {'server_ip': '0.0.0.0', 'port': 3306, 'db_type': 'mysql',
        'database_name': 'test', 'user': 'root', 'password': 'mysecretpassword'}
]


# sudo docker run --name dorm_test_mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
# sudo docker run --name dorm_postgres -p 5432:5432  -e  POSTGRES_PASSWORD=mysecretpassword -d postgres
