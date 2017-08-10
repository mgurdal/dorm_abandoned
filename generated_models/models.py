from database import models

class Node(models.Model):
    _id = models.PrimaryKey()
    server_ip = models.Char({'size': '15'})
    database_name = models.Char({'size': '255'})
    user = models.Char({'size': '255'})
    port = models.Integer()
    password = models.Char({'size': '255'})
    db_type = models.Char({'size': '255'})

