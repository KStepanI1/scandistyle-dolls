# Generated by Django 3.1.6 on 2021-02-21 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0005_auto_20210221_0621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file_id',
        ),
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(default=1, upload_to='', verbose_name='Файл'),
            preserve_default=False,
        ),
    ]
