from django.db import models

# Create your models here.

class Class(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    credit = models.IntegerField(default=0)
    option = (('GeneralCompulsory','通识必修'),
              ('Art','通识选修艺术类'),
              ('Society',"通识选修社科类"),
              ('Literature',"通识选修人文类"),
              ('Philosophy',"通识选修哲学类"),
              ('Others','非通识类'))




    category = models.CharField(max_length=1000,choices=option,default='非通识类')
    grade = models.IntegerField(default=0)

    prerequest = models.ManyToManyField("self", through='Prerequisite', symmetrical=False)

    def __str__(self):
        return self.name



class Department(models.Model):
    name = models.CharField(max_length=200)
    compulsoryCourse = models.ManyToManyField(Class,related_name='compulsory')
    selectiveCourse = models.ManyToManyField(Class,related_name='selective')
    required_selective_credit = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class User(models.Model):
    gender=( ('male',"男"),('female',"女"),)

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender,  default="男")
    credit_limit = models.IntegerField(default=10)
    c_time = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField(default=2018)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)





    def __str__(self):
        return self.name

    class Meta:
        ordering= ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Prerequisite(models.Model):
    course = models.ForeignKey(Class,on_delete=models.CASCADE,related_name='source')
    requisiteClass = models.ForeignKey(Class,on_delete=models.CASCADE,related_name='target')
    group_number = models.IntegerField(default=0)

    def __str__(self):
        return self.course.name + '的先修课为:' + self.requisiteClass.name





## 一节课可能有多个时间上课， 一个时间也有可能有多节课要上， 我们使用一个多对多的模型来试探一哈。
class Time(models.Model):
    day_choice =(('Mon',"星期一"),('Tue','星期二'),('Wed','星期三'),('Thu','星期四'),('Fri','星期五'),('Sat','星期六'),('Sun','星期天'))
    number_choice = (('1','第一大节'),('2','第二大节'),('3','第三大节'),('4','第四大节'),('5','第五大节'))
    day = models.CharField(max_length=100,choices=day_choice,default='Mon')
    number_choice = models.CharField(max_length=200,choices=number_choice,default='1')
    week = models.IntegerField(default=0)
    def __str__(self):
        tmp = None
        if self.week == 0:
            tmp = ""

        elif self.week == 1:
            tmp = "单周"

        else:
            tmp = '双周'

        return tmp+self.day+" "+self.number_choice

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    year_choice = ((2014,"2014-2015学年"),
                   (2015,"2015-2016学年"),
                   (2016,"2016-2017学年"),
                   (2017,"2017-2018学年"),
                   (2018,"2018-2019学年"))
    sememster_choice = (
        (1,"秋季学期"),
        (2,"春季学期"),
        (3,"夏季学期")
    )
    year = models.IntegerField(choices=year_choice,default=2018)
    sememster = models.IntegerField(choices=sememster_choice,default=1)
    lession = models.ForeignKey(Class,on_delete=models.CASCADE,default=None)
    teacher = models.CharField(max_length=200, default='')
    classroom = models.CharField(max_length=200,default='TBD')

    student = models.ManyToManyField(User,blank=True)
    capacity = models.IntegerField()
    time= models.ManyToManyField(Time)
    coursename = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.lession.code+" "+self.lession.name+" "+str(self.year)+" "+str(self.sememster)

class Score(models.Model):
    student = models.ForeignKey(User, on_delete= models.CASCADE)
    lession = models.ForeignKey(Course, on_delete= models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.student.name+" "+self.lession.coursename +" "+str(self.score)

