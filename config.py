import os, sys


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


MODEL_DIR = "/mymodels/"

CLUSTERS = [
    {'address':'127.0.0.1', 'name':'local_cluster_1', 'port':'40001'},
    {'address':'127.0.0.1', 'name':'local_cluster_2', 'port':'40002'},
    {'address':'127.0.0.1', 'name':'local_cluster_3', 'port':'40003'},
    {'address':'127.0.0.1', 'name':'local_cluster_4', 'port':'40004'},
]

NODES = [
        {'server_ip':'0.0.0.0', 'database_ip':'127.0.0.1', 'port': '-', 'type':'sqlite', 'database_name': 'datastore/poll_1.db', 'user':'-', 'password':'-'},
        {'server_ip':'0.0.0.0', 'database_ip':'127.0.0.1', 'port': 5432, 'type':'postgres', 'database_name': 'test', 'user': 'postgres', 'password':'mysecretpassword'},
        {'server_ip':'0.0.0.0', 'database_ip':'127.0.0.1', 'port': 3306, 'type':'mysql', 'database_name': 'test', 'user': 'root', 'password':'mysecretpassword'}
    ]


# sudo docker run --name dorm_test_mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
# sudo docker run --name dorm_postgres -p 5432:5432  -e  POSTGRES_PASSWORD=mysecretpassword -d postgres
