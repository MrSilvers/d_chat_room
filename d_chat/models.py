from django.db import models
from user_mgmt.models import *
# Create your models here.

class ChatRecordTbl(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    from_user_id = models.ForeignKey(UserTbl,related_name="form_user_id",on_delete=models.CASCADE)
    to_user_id = models.ForeignKey(UserTbl,related_name="to_user_id",on_delete=models.CASCADE)
    message = models.TextField(default='')
    public_flag = models.IntegerField(default=0)
