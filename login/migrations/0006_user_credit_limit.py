# Generated by Django 2.1.2 on 2018-12-09 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20181209_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credit_limit',
            field=models.IntegerField(default=10),
        ),
    ]