from django.db import models

# Create your models here.

class UserTbl(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.username

class UserFriendsTbl(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(UserTbl,on_delete=models.CASCADE,related_name="user")
    friend = models.ForeignKey(UserTbl,on_delete=models.CASCADE,related_name="user_friend")
    label = models.CharField(default="",max_length=64)
    group = models.CharField(default="",max_length=64)
    create_time = models.DateTimeField(auto_created=True)
    def __str__(self):
        return self.user.username

class GroupTbl(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(UserTbl,on_delete=models.CASCADE)
    group_name = models.CharField(max_length=64,default="")
    create_time = models.DateTimeField(auto_created=True)
