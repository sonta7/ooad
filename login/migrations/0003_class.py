# Generated by Django 2.1.2 on 2018-12-01 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20181129_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('credit', models.CharField(max_length=10)),
                ('student', models.ManyToManyField(to='login.User')),
            ],
        ),
    ]