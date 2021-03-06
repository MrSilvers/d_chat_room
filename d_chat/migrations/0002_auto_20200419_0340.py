# Generated by Django 2.0 on 2020-04-19 03:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_mgmt', '0002_grouptbl_userfriendstbl'),
        ('d_chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRecordDetailTbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_flag', models.BooleanField(default=True)),
                ('message', models.TextField(default='')),
                ('public_flag', models.IntegerField(default=0)),
                ('is_read_flag', models.BooleanField(default=False)),
                ('record_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('peer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peer_user', to='user_mgmt.UserTbl')),
            ],
        ),
        migrations.RenameField(
            model_name='chatrecordtbl',
            old_name='record_time',
            new_name='create_time',
        ),
        migrations.RemoveField(
            model_name='chatrecordtbl',
            name='from_flag',
        ),
        migrations.RemoveField(
            model_name='chatrecordtbl',
            name='is_read_flag',
        ),
        migrations.RemoveField(
            model_name='chatrecordtbl',
            name='message',
        ),
        migrations.RemoveField(
            model_name='chatrecordtbl',
            name='peer_user',
        ),
        migrations.RemoveField(
            model_name='chatrecordtbl',
            name='public_flag',
        ),
        migrations.AlterField(
            model_name='chatrecordtbl',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user_mgmt.UserTbl'),
        ),
        migrations.AddField(
            model_name='chatrecordtbl',
            name='record_detail',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='d_chat.ChatRecordDetailTbl'),
            preserve_default=False,
        ),
    ]
