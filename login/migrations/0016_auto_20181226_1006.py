# Generated by Django 2.1.4 on 2018-12-26 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20181226_0136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='coursename',
            field=models.CharField(max_length=100),
        ),
    ]
