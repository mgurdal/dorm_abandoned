import os, sys


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


MODEL_DIR = "/mymodels/"

CLUSTERS = [
    {'address':'127.0.0.1', 'name':'local_cluster_1', 'port':'40001'},
    {'address':'127.0.0.1', 'name':'local_cluster_2', 'port':'40002'},
    {'address':'127.0.0.1', 'name':'local_cluster_3', 'port':'40003'},
    {'address':'127.0.0.1', 'name':'local_cluster_4', 'port':'40004'},
]

DATABASES = {
    'sqlite': [
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_1.db', 'name':'poll_1.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_2.db', 'name':'poll_2.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_3.db', 'name':'poll_3.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_4.db', 'name':'poll_4.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_5.db', 'name':'poll_5.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_6.db', 'name':'poll_6.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_7.db', 'name':'poll_7.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_8.db', 'name':'poll_8.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_9.db', 'name':'poll_9.py'},
        {'host':'127.0.0.1', 'port': '-', 'database_name': 'datastore/poll_10.db', 'name':'poll_10.py'}
    ],

}

{
        'postgres': [
        {'database_name': 'test',
         'user': 'postgres',
         'password':'mysecretpassword',
         'host':'127.0.0.1',
         'port': 5432
        },
    ],
    'mysql': [
        {'database_name': 'employees',
         'user': 'root',
         'password':'mysecretpassword',
         'host':'127.0.0.1',
         'port': 3306
        },
    ]
}
# sudo docker run --name dorm_test_mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
# sudo docker run --name dorm_postgres -p 5432:5432  -e  POSTGRES_PASSWORD=mysecretpassword -d postgres
