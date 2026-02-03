from django.db import models


class Item(models.Model):
    name = models.CharField()
    desc = models.TextField()
    category = models.CharField()
    price = models.FloatField()
    is_active = models.BooleanField()

