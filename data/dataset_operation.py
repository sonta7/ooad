import pymysql
import numpy as np
import datetime
from read_course import file_reader, excel_read
from django.db import models


# classSet, departmentSet, teacherSet, classroomSet, courseList, weekTypeSet, timeSet = file_reader('./data/class_info.txt')
classSet, departmentSet, teacherSet, classroomSet, courseList, weekTypeSet, timeSet = excel_read(filename='./course.xlsx')

conn = pymysql.connect(host='localhost', user='root',password='yangsonglin9!',database='ooad3')
cursor = conn.cursor()

sqlInsert_department = 'insert into login_department(name, required_selective_credit) values (%s, %s)'
sqlInsert_teacher = 'insert into login_teachers(code, name, credits, category) values (%s,%s,%s,%s)'
sqlInsert_class = 'insert into login_class(code, name, credit, category, grade) values (%s,%s,%s,%s,%s)'
sqlInsert_time = 'insert into login_time(week, day, number_choice) values (%s,%s,%s)'
sqlInsert_user = "insert into login_user (name, password,email, sex, c_time,credit_limit, year,department_id) values (%s,%s,%s,%s,%s,%s,%s,%s)"
sqlInsert_class_department = "insert into login_department_compulsorycourse(department_id, class_id) select A.id, B.id from login_department A, login_class B where A.name=%s and B.code=%s"

sqlInsert_course = 'insert into login_course(teacher, classroom, coursename, capacity, sememster, year, lession_id) select %s,%s,%s,%s,%s,%s,A.id from login_class A where A.code=%s'
sqlInsert_course_time = 'insert into login_course_time(course_id, time_id) \
        select A.id, B.id from login_course A , login_class C, login_time B where A.lession_id=C.id and C.name=%s and A.coursename=%s and B.day=%s and B.number_choice=%s and B.week=%s'

sqlDelete_Department = "delete from login_department where name='人文科学中心' or name='体育中心' or name='公共基础课部' or name='公共基础课部' or name='思想政治教育与研究中心' or name='语言中心' or name='社会科学中心' or name='艺术中心' or name='高等教育研究中心' or name= '创新创业学院' or name='商学院'"
sqlSelect_Department = "select id from login_department"

# cursor.execute(sqlSelect_Department)
# res = cursor.fetchall()
# print(tuple(res[i][0] for i in range(len(res))))


def delete_departments():
    try:
        cursor.execute(sqlDelete_Department)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()  

def insert_Department():
    departments = tuple((de, 30) for de in departmentSet)
    print(departments)
    try:
        cursor.executemany(sqlInsert_department, departments)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def insert_Users():
    cursor.execute(sqlSelect_Department)
    res = cursor.fetchall()
    
    def insert_User():
        email = "empty"
        sex = "male"
        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        credit_limit = 30
        year = np.random.randint(2015,2019)     # generate different grades
        if year==2018:
            department_id = 1
        else:
            department_id = np.random.randint(2, 28)
        while department_id in [] :
            department_id = np.random.randint(2, 28)
        
        

        department_id = res[np.random.randint(len(res))]

        name = str("11") + str(year-2010) + str("1") + str(np.random.randint(1000, 9999)) 
        password = '123'
        email = str(name)+"@mail"
        try:
            cursor.execute(sqlInsert_user, (name, password, email, sex, c_time, credit_limit, year, department_id))
            # print((name, password, email , sex, c_time, credit_limit, year, department_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    department_id = res[np.random.randint(len(res))]
    for i in range(4*100):
        insert_User()
    try:
        cursor.execute(sqlInsert_user, ("CC", "CC", "CC@123", 'male', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 30, 2017, department_id ))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def insert_time():
    week_choice = (('0', '1-16周'), ('1', '单周'), ('2', '双周'))
    day_choice =(('Mon',"星期一"),('Tue','星期二'),('Wed','星期三'),('Thu','星期四'),('Fri','星期五'),('Sat','星期六'),('Sun','星期天'))
    number_choice = (('1','第一大节'),('2','第二大节'),('3','第三大节'),('4','第四大节'),('5','第五大节'))
    timelist = []
    for week in week_choice:
        for day in day_choice:
            for num in number_choice:
                timelist.append((week[0], day[0], num[0]))
    # print(timelist)
    
    try:
        cursor.executemany(sqlInsert_time, timelist)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def insert_class():
    classOptions = (('GeneralCompulsory','通识必修'),
            ('Art','通识选修艺术类'),
            ('Society',"通识选修社科类"),
            ('Literature',"通识选修人文类"),
            ('Philosophy',"通识选修哲学类"),
            ('Others','非通识类'))

    classlist = []

    for c in classSet:
        code = c[0]
        name = c[1]
        for grade in code:
            if grade<='9' and grade>='0':
                grade = int(grade)
                break
        
        period = c[2]
        credit = c[3]
        department = c[4]
        if department == '网络通识课程部':
            continue
        if department in ('体育中心', '思想政治教育与研究中心', '语言中心'):
            op = classOptions[0][0]
        elif department in ('艺术中心',):
            op = classOptions[1][0]
        elif department in ('社会科学中心', '创新创业学院', '高等教育研究中心'):
            op = classOptions[2][0]
        elif department in ('人文科学中心'):
            op = classOptions[3][0]
        elif department in ('公共基础课部'):
            op = classOptions[4][0]
        else:
            op = classOptions[5][0]
        classlist.append((code, name, credit, op, grade))
    try:
        cursor.executemany(sqlInsert_class, classlist)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
# insert_class()
def insert_department_class():
    dc_list = []
    for c in classSet:
        department = c[4]
        code = c[0]
        dc_list.append((department, code))
    try:
        cursor.executemany(sqlInsert_class_department, dc_list)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def insert_course(year=2018):
    # teacher, capacity, classroom, sememster, year, lessionid
    courses = []
    for co in courseList:
        code = co.code
        classname = co.classname
        coursename = co.coursename
        department = co.department
        period = co.period
        credits = co.credits
        teachers = co.teachers
        classtimes = co.classtimes
        classrooms = co.classrooms
        time_room = co.time_room
        # print(code, classname, coursename, department, period, credits, teachers, classtimes, classrooms, time_room)
        # print((' '.join(teachers), 100, ' '.join(classrooms), 1, 2018, code))
        # break

        # print((' '.join(teachers).strip(), ' '.join(classrooms).strip(), coursename, 100, 1, 2018, code))
        courses.append((' '.join(teachers).strip(), ' '.join(classrooms).strip(), coursename, 100, 1, year, code))
    try:
        cursor.executemany(sqlInsert_course, courses)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

# insert_course()
def insert_course_time():
    course_time_list = []
    for co in courseList:
        classname = co.classname
        coursename = co.coursename
        times = co.classtimes

        for t in times:
            day = t[1]
            period = t[2]
            week = t[0]
            course_time_list.append((classname, coursename, day, period, week))
    # print(course_time_list)
    
    try:
        for t in course_time_list:
            print(t)
            cursor.execute(sqlInsert_course_time, t)
        # cursor.executemany(sqlInsert_course_time, course_time_list)
        conn.commit()
    except Exception as e:
        # print(course_time_list)
        print('err', t)
        print(e)
        conn.rollback()

def insert_database():
    insert_Department()
    delete_departments()
    insert_Users()
    insert_time()

    insert_class()
    insert_department_class()
    insert_course(2018)
    insert_course_time()
    insert_course(2017)

def insert_preclasses():
    # codeA, codeB, group
    preclasses = []
    preclasses.append(()) 
    
    sql = 'insert into login_prerequisite(course_id, requisiteClass_id, group_number) select A.id, B.id, %s from login_class A, login_class B where A.code=%s and B.code=%s'
    
    try:
        cursor.executemany(sql, preclasses)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()



score_list = [
    (100, 'CS101A', 'CC'),
    (100, 'CS102A', 'CC'),
    (100, 'CS203', 'CC'),
    (100, 'CS205', 'CC'),
    (100, 'CS207', 'CC'),
    (100, 'CS209A', 'CC'),
]

def insert_score():
    sql = "insert login_score (lession_id, student_id, score)   \
            select A.id as course_id, B.id as user_id, %s from login_course A, login_user B, login_class C where C.code=%s and B.name=%s and A.lession_id=C.id and A.year=2017 limit 1"

    try:
        cursor.executemany(sql, score_list)
        conn.commit()
    except  Exception as e:
        print(e)
        conn.rollback()
    
# insert_score()


insert_database()
# insert_Users()
# insert_time()
# insert_Department()
# delete_departments()

# insert_course()
# insert_course_time()

# insert_course(2017)s