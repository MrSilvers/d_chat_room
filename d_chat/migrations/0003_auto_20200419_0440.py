# Generated by Django 2.0 on 2020-04-19 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d_chat', '0002_auto_20200419_0340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatrecordtbl',
            name='record_detail',
        ),
        migrations.AddField(
            model_name='chatrecorddetailtbl',
            name='chat_record',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='d_chat.ChatRecordTbl'),
            preserve_default=False,
        ),
    ]
