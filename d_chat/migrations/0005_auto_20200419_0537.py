# Generated by Django 2.0 on 2020-04-19 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d_chat', '0004_auto_20200419_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatrecorddetailtbl',
            name='chat_record',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='d_chat.ChatRecordTbl'),
        ),
    ]