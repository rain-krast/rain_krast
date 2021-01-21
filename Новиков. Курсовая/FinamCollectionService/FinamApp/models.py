from django.db import models

class Article(models.Model):
    source = models.CharField(max_length=350)
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    text = models.TextField()
