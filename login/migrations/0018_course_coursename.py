# Generated by Django 2.1.4 on 2018-12-26 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_auto_20181226_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='coursename',
            field=models.CharField(default='', max_length=100),
        ),
    ]
