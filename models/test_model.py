from dorm.database import models

class Testmodel(models.Model):
    test_int = models.Integer()
    id = models.PrimaryKey()

