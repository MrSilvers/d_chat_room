from django.db import models

# Create your models here.

class UserTbl(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
