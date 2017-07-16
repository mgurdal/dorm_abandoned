from dorm.database import models

class Testmodel(models.Model):
    id = models.PrimaryKey()
    test_int = models.Integer()

