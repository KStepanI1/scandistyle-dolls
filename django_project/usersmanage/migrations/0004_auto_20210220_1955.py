# Generated by Django 3.1.6 on 2021-02-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0003_item_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='file',
            field=models.CharField(max_length=200, verbose_name='Файл file_id'),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]