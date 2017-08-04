from database import models

class Node(models.Model):
    _id = models.PrimaryKey()
    port = models.Integer()
    db_type = models.Char({'size': '255'})
    database_name = models.Char({'size': '255'})
    server_ip = models.Char({'size': '15'})
    user = models.Char({'size': '255'})
    password = models.Char({'size': '255'})

