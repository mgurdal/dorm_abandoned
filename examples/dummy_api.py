from sanic import Sanic
from sanic.response import json

app = Sanic()

DATABASES = {
    'sqlite': [
        {'database_name': 'datastore/poll_1.db', 'name':'poll_1.py'},
        {'database_name': 'datastore/poll_2.db', 'name':'poll_2.py'},
        {'database_name': 'datastore/poll_3.db', 'name':'poll_3.py'},
    ],
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

@app.route("/databases")
async def test(request):
    return json(DATABASES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)