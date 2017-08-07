from database import models

class Table_2(models.Model):
    id = models.PrimaryKey()


class Table_3(models.Model):
    id = models.PrimaryKey()


class Table_1(models.Model):
    id = models.PrimaryKey()
    datetime_1 = models.Datetime()
    fk_1 = models.ForeignKey(Table_2)
    date_1 = models.Date()
    varchar_1 = models.Varchar({'size': '200'})
    char_1 = models.Char({'size': '200'})


class Table_3_Table_1(models.Model):
    id = models.PrimaryKey()
    table_3_id = models.ForeignKey(Table_3)
    table_1_id = models.ForeignKey(Table_1)


class Node(models.Model):
    _id = models.PrimaryKey()
    database_name = models.Char({'size': '255'})
    user = models.Char({'size': '255'})
    server_ip = models.Char({'size': '15'})
    db_type = models.Char({'size': '255'})
    password = models.Char({'size': '255'})
    port = models.Integer()

