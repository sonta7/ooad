# Generated by Django 2.1.4 on 2018-12-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_merge_20181225_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='coursename',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]