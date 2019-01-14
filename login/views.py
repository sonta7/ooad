from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from . import forms
from django.shortcuts import HttpResponse
# Create your views here.
from login import models
import json
import itertools
import math
from django.db.models import Q




year = 2018
sememster = 1
crossyear_protection = False
available_to_choose = True



def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    user = models.User.objects.get(name=request.session['user_name'])


    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login',None):
        return redirect("/index/")

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']


            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login']=True
                    request.session['user_id'] = user.id
                    request.session['user_name']=user.name
                    request.session['major'] = user.department.name
                    request.session['grade'] = int(year) - int(user.year) + 1
                    return redirect('/index/')
                else:
                    message= "密码不正确"

            except:
                message = "用户不存在！"


        return render(request,'login.html',locals())


    login_form = forms.UserForm()
    return render(request,'login.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()

    return redirect("/login/")

def dropout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    models.User.objects.get(name=request.session.get('user_name')).delete()
    request.session.flush()

    return redirect("/login/")


def classselect(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    user = models.User.objects.get(name=request.session.get('user_name'))

    if request.method == 'GET':
        classes = models.Course.objects.all()
        courses = models.Course.objects.filter(student=user,sememster=sememster,year=year)
        score1 = user.credit_limit


        want = user.department.compulsoryCourse.all()
        want = want | user.department.selectiveCourse.all()
        want = want | models.Class.objects.filter(category='GeneralCompulsory')
        want = want.filter(grade=request.session['grade'])
        selected_class = models.Course.objects.filter(student=user)
        selected_course = models.Class.objects.filter(~Q(course__in=selected_class))
        selected_course = selected_course & want



        return render(request,'classselect.html',locals())

    elif request.method == 'POST':
        try:
            want = request.POST['lastname']
            candidate = models.Class.objects.filter(Q(code=want)|Q(name=want))

            if len(candidate.all()) == 0:

                return HttpResponse("你输入的课程名字或者代码有丶问题")
            else:
                b = candidate.get()
                selected_class = models.Course.objects.filter(student=user)
                selected_course = models.Class.objects.filter(Q(course__in=selected_class))
                if b in selected_course:
                    return HttpResponse("选过了呀")

                c = models.Course.objects.filter(Q(lession=b) & ~Q(capacity=0))
                if len(c) == 0:
                    return HttpResponse("没得课了，滚啊")




            return HttpResponse("OK"+b.name)

        except:

            want = request.POST.getlist('usertype','')
            credit = 0
            print("i wanna",want,len(want))
            if len(want) == 0:
                return HttpResponse("您没有选择任何课程，使用CONTROL+A在下面的框中进行多选。")
            for i in want:
                credit+= models.Class.objects.get(name=i).credit
                if models.Class.objects.get(name=i) in models.Class.objects.filter(course__student=user):
                    return HttpResponse("您已经选过了"+i+"噢")

                cou = models.Class.objects.get(name=i)
                if cou.grade!=0 and cou.grade!=request.session['grade'] and crossyear_protection==True:
                    return HttpResponse(i + "现在处于跨年级选课保护状态，不能选噢")


            if credit>user.credit_limit:
                return HttpResponse("不能够超出学分选课噢")

            bixiu = user.department.compulsoryCourse.all()
            bixiu = bixiu | models.Class.objects.filter(category="GeneralCompulsory")


            bixiukecheng = []
            qitakecheng = []

            for i in want:
                if models.Class.objects.get(name=i) in bixiu:
                    bixiukecheng.append(i)
                else:
                    qitakecheng.append(i)


            ###################写一个直接暴力求解的算法？

            all_bixiu = []

            for i in bixiukecheng:
                tmp_course = models.Course.objects.filter(lession__name=i).values_list()
                all_bixiu.append([a[0] for a in tmp_course])



            final_result = []
            def digui(j,final_result,tmp_result):
                if j == -1:
                    final_result.append(tmp_result[:])
                    return

                times = len(all_bixiu[j])
                for i in range(times):
                    tmp_result2 = tmp_result[:]
                    tmp_result2.append(all_bixiu[j][i])
                    digui(j-1,final_result,tmp_result2[:])

            digui(len(all_bixiu)-1,final_result,[])




            def subsets( nums):
                if not nums:
                    return [[]]

                ret = []
                ret.extend(subsets(nums[1:]))
                for i in range(len(ret)):
                    ret.append([nums[0]] + ret[i])

                return ret

            all_candidate = []
            for i in range(len(final_result)):
                all_candidate.extend(subsets(nums=final_result[i]))

            all_candidate.sort()
            d = list(k for k, _ in itertools.groupby(all_candidate))
            d.sort(key=len,reverse=True)

            final_len = 0

            for i in range(len(d)):
                tmp = d[i]
                times = []
                for j in range(len(tmp)):
                    time = models.Time.objects.filter(course__id=tmp[j])
                    for t in time:
                        times.append(t.id)

                if len(times) ==  len(set(times)):
                    dict = {}
                    for i in range(0, 25):
                        dict[i] = []

                    for i in times:
                        dict[i % 25].append(i)

                    flag = 0
                    for i in range(1, 25):
                        if len(dict[i]) > 1:
                            if i in dict[i]:
                                flag = 1
                                break

                    if len(dict[0]) > 1 and 25 in dict:
                        flag = 1

                    if flag == 0:
                        final_len = len(tmp)
                        break

            #########################然后考虑所有的，能有

            consideration = [item for item in d if len(item) == final_len]
            ok = []
            for i in range(len(consideration)):
                tmp = consideration[i]
                times = []
                for j in range(len(tmp)):
                    time = models.Time.objects.filter(course__id=tmp[j])
                    for t in time:
                        times.append(t.id)

                if len(times) ==  len(set(times)):
                    dict = {}
                    for i in range(0,25):
                        dict[i] = []

                    for i in times:
                        dict[i%25].append(i)

                    flag = 0
                    for i in range(1,25):
                        if len(dict[i]) > 1:
                            if i in dict[i]:
                                flag = 1
                                break

                    if len(dict[0]) > 1 and 25 in dict:
                        flag = 1

                    if flag == 0:





                        final_len = len(times)
                        ok.append(tmp)

            final_final = []
            for okk in ok:
                all_xuanxiu = []
                time = models.Time.objects.filter(course__id__in=okk)
                time2 = models.Time.objects.filter(course__id__in=okk)
                for i in time2:
                    if i.week == 0:
                        time = time | models.Time.objects.filter(day = i.day, number_choice= i.number_choice)

                    elif i.week == 1 or i .week==2:
                        time = time | models.Time.objects.filter(day = i.day, number_choice= i.number_choice, week = 0)


                for j in qitakecheng:
                    tmp_course = models.Course.objects.filter(Q(lession__name=j) & ~ Q(time__in=time)).values_list()
                    all_xuanxiu.append([a[0] for a in tmp_course])


                final_result = []
                def digui(j,final_result,tmp_result):
                    if j == -1:
                        final_result.append(tmp_result[:])
                        return

                    times = len(all_xuanxiu[j])
                    for i in range(times):
                        tmp_result2 = tmp_result[:]
                        tmp_result2.append(all_xuanxiu[j][i])
                        digui(j-1,final_result,tmp_result2[:])

                digui(len(all_xuanxiu)-1,final_result,[])




                def subsets( nums):
                    if not nums:
                        return [[]]

                    ret = []
                    ret.extend(subsets(nums[1:]))
                    for i in range(len(ret)):
                        ret.append([nums[0]] + ret[i])

                    return ret

                all_candidate = []
                for i in range(len(final_result)):
                    all_candidate.extend(subsets(nums=final_result[i]))

                all_candidate.sort()
                d = list(k for k, _ in itertools.groupby(all_candidate))
                d.sort(key=len,reverse=True)

                final_ans = []

                for i in range(len(d)):
                    tmp = d[i]
                    times = []
                    for j in range(len(tmp)):
                        time = models.Time.objects.filter(course__id=tmp[j])
                        for t in time:
                            times.append(t.id)

                    if len(times) ==  len(set(times)):
                        dict = {}
                        for j in range(0, 25):
                            dict[j] = []

                        for j in times:
                            dict[j % 25].append(j)

                        flag = 0
                        for j in range(1, 25):
                            if len(dict[j]) > 1:
                                if j in dict[j]:
                                    flag = 1
                                    break

                        if len(dict[0]) > 1 and 25 in dict:
                            flag = 1

                        if flag == 0:
                            final_ans = tmp
                            break

                final_final.append([okk,final_ans])


                #########################然后考虑所有的，能有



            final_final.sort(key=lambda k: len(k[1]),reverse=True)

            final_choosen = final_final[0]

            final_compulsory = final_choosen[0]
            final_selective = final_choosen[1]

            for i in final_compulsory:
                course = models.Course.objects.get(id = i)
                course.capacity-=1
                course.student.add(user)
                course.save()
                user.credit_limit -= course.lession.credit
                user.save()

            for i in final_selective:

                course = models.Course.objects.get(id=i)

                course.capacity -= 1
                course.student.add(user)
                course.save()
                user.credit_limit -= course.lession.credit
                user.save()
            

            return HttpResponse("一键选课成功辣")




def classwithdraw(request):

    if not request.session.get('is_login',None):
        return redirect('/login/')

    if request.method == 'GET':
        classes = models.Course.objects.all()
        user = models.User.objects.get(name=request.session.get('user_name'))
        courses = models.Course.objects.filter(student=user,sememster=sememster,year=year)
        score1 = user.credit_limit

        return render(request,'classwithdraw.html',locals())



def show_score(request,select_year,select_sememster):
    if request.method == 'GET':
        user = models.User.objects.get(name=request.session['user_name'])

        grade = models.Score.objects.filter(student=user, lession__year=select_year,lession__sememster=select_sememster)
        response_data = {'total': grade.count(), 'rows': []}
        for i in grade:
            response_data['rows'].append({
                "coursecode": i.lession.lession.code,
                "coursename": i.lession.lession.name,
                "score": i.score
            }
        )
        return HttpResponse(json.dumps(response_data))

def show_pyfa(request,department,type):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    if request.method == 'GET':
        user = models.User.objects.get(name=request.session['user_name'])

        selected_course = models.Course.objects.filter(student=user)

        if type=='compulsory' or type=='selective':

            dep = models.Department.objects.get(name=department)
            if type=='compulsory':
                course = dep.compulsoryCourse.all()
            elif type=='selective':
                course = dep.selectiveCourse.all()
            response_data = {'total': course.count(), 'rows': []}
            for i in course:
                finished = False
                majoring = False
                for j in  selected_course :
                    if i == j.lession:
                        if j.sememster == sememster and j.year == year:
                            majoring = True

                        else:
                            finished = True
                        break

                status = ""
                if majoring:
                    status = "正在修读"
                elif finished:
                    status = "已修读"
                else:
                    status = "未修读"
                response_data['rows'].append(
                    {
                        "coursecode": i.code,
                        "coursename": i.name,
                        "credit":i.credit,
                        "finish": status,
                    }
                )



            return  HttpResponse(json.dumps(response_data))

        else:
            if department=='compulsory':

                courses = models.Class.objects.filter(category='GeneralCompulsory')
            elif department=='selective':

                courses = models.Class.objects.filter(category=type)

            response_data = {'total': courses.count(), 'rows': []}

            for i in courses:
                finished = False
                for j in selected_course:
                    if i == j.lession:
                        finished = True
                        break

                response_data['rows'].append(
                    {
                        "coursecode": i.code,
                        "coursename": i.name,
                        "credit": i.credit,
                        "finish": "已完成" if finished else "未完成"
                    }
                )
            return HttpResponse(json.dumps(response_data))




def show_course(request,select):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    user = models.User.objects.get(name=request.session['user_name'])

    if request.method == "GET":
        limit = request.GET.get('limit')   # how many items per page
        offset = request.GET.get('offset')  # how many items in total in the DB
        search = request.GET.get('search')
        status = request.GET.get('status')
        if search and select!='withdraw':    #    判断是否有搜索字

            all_records = models.Course.objects.filter(teacher=search,sememster=sememster,year=year)
            try:
                candidate_class = models.Class.objects.filter(Q(code__contains=search)|Q(name__contains=search))

                for c in candidate_class:

                    all_records = all_records | (models.Course.objects.filter(lession=c,sememster=sememster,year=year))

            except:
                pass

            if status == '通识选修':
                all_records = all_records.filter(Q(lession__category='Art')|Q(lession__category='Society')|Q(lession__category='Literature'
                                                ) | Q(lession__category='Philosophy'))
            elif status == '本学期计划选课':
                if request.session['grade']==1:
                    all_records = all_records.filter(Q(lession__category='GeneralCompulsory'))



                    major_course = user.department.compulsoryCourse.all()
                    major_course = major_course.filter(grade=request.session['grade'])
                    for i in major_course:
                        all_records = all_records | models.Course.objects.filter(lession=i,year=year,sememster=sememster)

                else:
                    all_recordss = None
                    major_course = user.department.compulsoryCourse.all()
                    major_course = major_course.filter(grade=request.session['grade'])


                    for i in major_course:
                        if all_recordss == None:
                            all_recordss = models.Course.objects.filter(lession=i,year=year,sememster=sememster)
                        else:
                            all_recordss = all_recordss | models.Course.objects.filter(lession=i,year=year,sememster=sememster)

                    all_records = all_records & all_recordss

            elif status == '专业跨年级':
                major_course = user.department.compulsoryCourse.all()
                major_course = major_course.filter(~Q(grade=request.session['grade']))
                selective_course = user.department.selectiveCourse.all()
                selective_course = selective_course.filter(~Q(grade=request.session['grade']))
                major_course = major_course | selective_course
                all_recordss = None
                for i in major_course:
                    if all_recordss == None:
                        all_recordss = models.Course.objects.filter(lession=i,year=year,sememster=sememster)
                    else:
                        all_recordss = all_recordss | models.Course.objects.filter(lession=i,year=year,sememster=sememster)

                all_records = all_records & all_recordss














        elif select=='select':

            all_records = models.Course.objects.filter(sememster=sememster,year=year)   # must be wirte the line code here
            if status == '通识选修':
                all_records = all_records.filter(Q(lession__category='Art')|Q(lession__category='Society')|Q(lession__category='Literature'
                                                ) | Q(lession__category='Philosophy'))
            elif status == '本学期计划选课':
                if request.session['grade']==1:
                    all_records = all_records.filter(Q(lession__category='GeneralCompulsory'))



                    major_course = user.department.compulsoryCourse.all()
                    major_course = major_course.filter(grade=request.session['grade'])
                    selective_course = user.department.selectiveCourse.all()
                    selective_course = selective_course.filter(grade=request.session['grade'])
                    major_course = major_course | selective_course
                    for i in major_course:
                        if all_records == None:

                            all_records =  models.Course.objects.filter(lession=i,year=year,sememster=sememster)
                        else:
                            all_records = all_records | models.Course.objects.filter(lession=i,year=year,sememster=sememster)





                else:
                    all_records = None
                    major_course = user.department.compulsoryCourse.all()
                    major_course = major_course.filter(grade=request.session['grade'])
                    selective_course = user.department.selectiveCourse.all()
                    selective_course = selective_course.filter(grade=request.session['grade'])
                    major_course = major_course | selective_course

                    for i in major_course:
                        if all_records == None:
                            all_records = models.Course.objects.filter(lession=i,year=year,sememster=sememster)
                        else:
                            all_records = all_records | models.Course.objects.filter(lession=i,year=year,sememster=sememster)

            elif status == '专业跨年级':
                major_course = user.department.compulsoryCourse.all()
                major_course = major_course.filter(~Q(grade=request.session['grade']))
                selective_course = user.department.selectiveCourse.all()
                selective_course = selective_course.filter(~Q(grade=request.session['grade']))
                major_course = major_course | selective_course
                all_records = None
                for i in major_course:
                    if all_records == None:
                        all_records = models.Course.objects.filter(lession=i,year=year,sememster=sememster)
                    else:
                        all_records = all_records | models.Course.objects.filter(lession=i,year=year,sememster=sememster)






        elif select=='withdraw':
            all_records = models.Course.objects.filter(student=user,year=year,sememster=sememster)

        # elif select=="withdraw":
        #     all_records = models.Course.objects.filter(student=user)
        all_records_count = all_records.count()
        if not offset:
            offset = 0
        if not limit:
            limit = 20    # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(all_records, limit)   # 开始做分页
        page = int(int(offset) / int(limit) + 1)
        response_data = {'total':all_records_count,'rows':[]}
        # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容





        for course in pageinator.page(page):
            time = models.Time.objects.filter(course=course)
            timeres = ""
            for time1 in time:

                if time1.week == 0:
                    a = ""
                elif time1.week == 1:
                    a = '单周'

                else:
                    a = '双周'

                timeres+= a+time1.day+" "+time1.number_choice
                timeres+= "\n"
            response_data['rows'].append({
                "courseid":course.id,
                "coursecode":course.lession.code,
                "coursename":course.coursename,

                "teacher":course.teacher,
                "classroom":course.classroom,
                "credit":course.lession.credit,
                "time": timeres,
                "capacity":course.capacity
            })

        return HttpResponse(json.dumps(response_data))

def deleteC(request,a):
    course = models.Course.objects.get(id = a)

    user = models.User.objects.get(name=request.session['user_name'])
    selected_course = models.Course.objects.filter(student=user,year=year,sememster=sememster)
    if course not in selected_course:
        return HttpResponse("你没有选这门课..")
    pre = models.Prerequisite.objects.filter(requisiteClass=course.lession)

    for c in selected_course:
        for i in pre:
            if c.lession == i.course:

                return HttpResponse("您选的"+c.lession.name+"需要该课程作为先修课，不能退。")



    course.student.remove(user)
    course.capacity+=1
    course.save()
    user.credit_limit+=course.lession.credit
    user.save()
    return HttpResponse("退课成功")




def getC(request,a):
    course = models.Course.objects.get(id=a)
    if course.capacity==0:
        return HttpResponse("课余量不足")
    else:
       user = models.User.objects.get(name=request.session['user_name'])
       if course.lession.credit > user.credit_limit:
           return HttpResponse("超过学分限制选课，选课失败")

       if course.lession.grade!=0 and course.lession.grade != request.session['grade'] and crossyear_protection==True:
           return HttpResponse("您好,当前选课时段不允许跨年级选课.")
       user_selected = models.Course.objects.filter(student=user)

       is_selected_flag = False
       for all_possible_course in models.Course.objects.filter(lession=course.lession):
           if all_possible_course in user_selected:
               is_selected_flag = True
               break

       if not is_selected_flag:
           a = models.Time.objects.filter(course__student=user)

           b = models.Time.objects.filter(course=course)


           for lession in b:
               if lession.week == 0:
                   lessions = models.Time.objects.filter(day=lession.day,number_choice=lession.number_choice)
                   for lession2 in lessions:
                       if lession2 in a:
                           cour = models.Course.objects.get(time=lession2, student=user)
                           return HttpResponse("跟  " + cour.lession.name + "  时间冲突，不能选择。")

               elif lession.week == 1 or lession.week == 2:
                   lession_2 = models.Time.objects.get(day=lession.day,number_choice=lession.number_choice,week=0)

                   if lession in a:
                       cour = models.Course.objects.get(time=lession, student=user)
                       return HttpResponse("跟  " + cour.lession.name + "  时间冲突，不能选择。")
                   if lession_2 in a:
                       cour = models.Course.objects.get(time=lession_2, student=user)
                       return HttpResponse("跟  " + cour.lession.name + "  时间冲突，不能选择。")




           prerequisites =  models.Prerequisite.objects.filter(course=course.lession)

           if len(prerequisites)!=0:
               dict = {}
               dict2 = {}
               for pre in prerequisites:
                   if dict.get(pre.group_number,None) ==  None:
                       dict[pre.group_number] = 0
                       dict2[pre.group_number] = []
                   dict2[pre.group_number].append(pre.requisiteClass.name)

                   if dict.get(pre.group_number) == 1:
                       continue
                   flag = 0
                   for a in models.Course.objects.filter(lession = pre.requisiteClass):
                       if a in user_selected:
                           flag = 1
                           break
                   if flag == 0:
                       dict[pre.group_number]=1

               if 0 not in dict.values():
                   str = "先修课程尚未修足,您需要修的先修课有"

                   length = len(dict2)
                   count = 1
                   for a in dict2.values():
                       str += "("
                       for b in a:

                           if b!= a[-1]:
                               str+= b
                               str+='  and  '
                           else:
                               str+= b
                               str+= ')'

                       if count != length:
                           str+='  or   '
                           count+=1








                   return HttpResponse(str)






           course.capacity -=1
           course.student.add(user)
           course.save()
           user.credit_limit-=course.lession.credit
           user.save()
           return HttpResponse("选课成功")
       else:
           return HttpResponse("您本学期或者之前已经选择了该课程。")
    return HttpResponse(a)


def lookup(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    user = models.User.objects.get(name=request.session['user_name'])
    if request.method=='GET':
        course = models.Score.objects.filter(student=user)
        year0 = year+1
        year1 = year
        year2 = year-1
        year3 = year-2
        year4 = year-3
        if sememster == 1:
            sem1 = sememster
        elif sememster == 2:
            sem2 = sememster
        else:
            sem3 = sememster


        return render(request,"lookup.html",locals())

    elif request.method=='POST':
        relative = request.POST['selection']
        if int(relative)<0:
            select_year = year
            select_sememster = sememster - int(relative)
        else:
            select_year = year - math.ceil(int(relative)/3.0)
            a = (int(relative) % 3)
            if a==0:
                select_sememster = 1
            elif a==1:
                select_sememster = 3
            else:
                select_sememster = 2

        grade = models.Score.objects.filter(student=user, student__course__year=select_year,
                                            student__course__sememster=select_sememster)
        response = []

        course = models.Course.objects.filter(student=user,year=select_year, sememster=select_sememster)
        for i in grade:
            response.append({
                "coursecode": i.lession.lession.code,
                "coursename": i.lession.lession.name,
                "score": i.score
            }
        )






        return render(request,'showScore.html',locals())




def lookuppyfa(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    user = models.User.objects.get(name=request.session['user_name'])
    if request.method == 'GET':
       department = models.Department.objects.all()
       return render(request,'lookuppyfa.html',locals())

    elif request.method=='POST':

        selection = request.POST['selection']
        category = request.POST['type']
        if selection == 'compulsory':
            general =  'compulsory'
            para = 'hello'
            return render(request, 'showgeneralpyfa.html', locals())
        elif selection=='selective':
            general = 'selective'
            if category=='艺术':
                para = 'Art'
            elif category=='社科':
                para = 'Society'
            elif category=='哲学':
                para = 'Philosophy'
            else:
                para = 'Literature'
            return render(request,'showgeneralpyfa.html',locals())

        dep = models.Department.objects.get(name=selection)

        return render(request,'showpyfa.html',locals())

