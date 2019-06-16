# -*- encoding=utf8 -*-


from django.db import models

# Create your models here.
class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True)
    nickname = models.CharField(max_length=256)
    focus_cities = models.TextField(default='[]')
    focus_constellations = models.TextField(default='[]')
    focus_stocks = models.TextField(default='[]')
    shebeiid = models.CharField(max_length=32)