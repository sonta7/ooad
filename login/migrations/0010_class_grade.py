# Generated by Django 2.1.2 on 2018-12-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20181215_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='grade',
            field=models.CharField(choices=[(1, '大一'), (2, '大二'), (3, '大三'), (4, '大四'), (5, '不限')], default='不限', max_length=1000),
        ),
    ]
