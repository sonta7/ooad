# Generated by Django 2.1.2 on 2018-12-23 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_class_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='grade',
            field=models.IntegerField(default=0),
        ),
    ]
