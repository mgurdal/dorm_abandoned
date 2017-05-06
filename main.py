"""
Create models here
"""

from database import models
from datetime import datetime

class Category(models.Model):
    """ Blog categories """
    name = models.CharField(max_lenth=255)

class Post(models.Model):
    """Blog Post"""
    title = models.CharField(max_lenth=255)
    body = models.TextField()
    category = models.ManyToManyField(Category)
    creation_date = models.DateTimeField()


if __name__ == "__main__":
    DB = models.Sqlite("blog.db")
    DB.create_table(Post)
    #post = Post(title="ORM", body="Some Text", publish_date=datetime.now())
    #post.save()
    """
    for cat in ["python", "orm"]:
        c = Category(cat)
        c.save()
        post.category.add(c)"""
    
