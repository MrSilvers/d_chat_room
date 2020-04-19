from django.db import models
from user_mgmt.models import *
from django.utils import timezone
# Create your models here.

class ChatRecordTbl(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserTbl,related_name="chat_record_user",on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username

class ChatRecordDetailTbl(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    chat_record = models.ForeignKey(ChatRecordTbl,default=1,null=True,on_delete=models.SET_NULL)
    peer_user = models.ForeignKey(UserTbl,related_name="chat_record_detail_peer_user",on_delete=models.CASCADE)
    from_flag = models.BooleanField(default=True)
    message = models.TextField(default='')
    public_flag = models.IntegerField(default=0)
    is_read_flag = models.BooleanField(default=False)
    record_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-record_time",)
        
    def __str__(self):
        if self.from_flag:
            return self.chat_record.user.username + " Say: " + self.message[:40]
        else:
            return self.chat_record.user.username + " Receive: " + self.message[:40]



class GroupChatRecordTbl(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(GroupTbl,on_delete=models.CASCADE)
    user = models.ForeignKey(UserTbl,on_delete=models.CASCADE)
    record = models.TextField(default='')
    record_time = models.DateTimeField(default=timezone.now)




