# Generated by Django 2.1.2 on 2018-12-14 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_user_credit_limit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('required_selective_credit', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='class',
            name='student',
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('GeneralCompulsory', '通识必修'), ('Art', '通识选修艺术类'), ('Society', '通识选修社科类'), ('Literature', '通识选修人文类'), ('Philosophy', '通识选修哲学类'), ('Others', '非通识类')], default='非通识类', max_length=1000),
        ),
        migrations.AddField(
            model_name='course',
            name='classroom',
            field=models.CharField(default='TBD', max_length=200),
        ),
        migrations.AddField(
            model_name='course',
            name='sememster',
            field=models.IntegerField(choices=[(1, '秋季学期'), (2, '春季学期'), (3, '夏季学期')], default=1),
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.IntegerField(choices=[(2014, '2014-2015学年'), (2015, '2015-2016学年'), (2016, '2016-2017学年'), (2017, '2017-2018学年'), (2018, '2018-2019学年')], default=2018),
        ),
        migrations.AddField(
            model_name='user',
            name='year',
            field=models.IntegerField(default=2018),
        ),
        migrations.AlterField(
            model_name='score',
            name='lession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Course'),
        ),
        migrations.AddField(
            model_name='department',
            name='compulsoryCourse',
            field=models.ManyToManyField(related_name='compulsory', to='login.Class'),
        ),
        migrations.AddField(
            model_name='department',
            name='selectiveCourse',
            field=models.ManyToManyField(related_name='selective', to='login.Class'),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.Department'),
            preserve_default=False,
        ),
    ]
