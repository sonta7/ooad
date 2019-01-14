# Generated by Django 2.1.4 on 2018-12-27 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_auto_20181227_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_room_time',
            name='course',
        ),
        migrations.RemoveField(
            model_name='course_room_time',
            name='room',
        ),
        migrations.RemoveField(
            model_name='course_room_time',
            name='time',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='classroom',
            field=models.CharField(default='TBD', max_length=200),
        ),
        migrations.DeleteModel(
            name='Classroom',
        ),
        migrations.DeleteModel(
            name='Course_room_time',
        ),
        migrations.DeleteModel(
            name='Teachers',
        ),
    ]