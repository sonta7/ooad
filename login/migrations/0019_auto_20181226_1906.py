# Generated by Django 2.1.4 on 2018-12-26 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_course_coursename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='coursename',
        ),
        migrations.AddField(
            model_name='time',
            name='week',
            field=models.IntegerField(default=0),
        ),
    ]
