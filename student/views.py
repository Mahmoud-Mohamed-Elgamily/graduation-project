from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .student import *
from django.template.defaulttags import register

# Create your views here.
@login_required
def tbl(request):
    if request.method =="GET":
        one="الفترة/اليوم"
        two="السبت"
        three="الاحد"
        Four="الاثنين"
        five="الثلاثاء"
        six="الاربعاء"
        seven="الخميس"
        titles=[ [one,""] , [two,""] , [three,""] , [Four,""] , [five,""] , [six,""] , [seven,""] ]
        one="الاولي"
        two="الثانية"
        three="الثالثة"
        Four="الرابعة"
        interval=[ [ [one,""],[","],[","],[","],[","],[","],[","]],[[two,""],[","],[","],[","],[","],[","],[","]],[[three,""],[","],[","],[","],[","],[","],[","]],[ [Four,""],[","],[","],[","],[","],[","],[","]]]
        tabl=table(request.user.pk)
        for lecs in tabl[0]:
            lec=tabl[0][lecs][1]
            interval[int(lec[0])-1][int(lec[1])]=[ "محاضرة"+"<br>"+tabl[0][lecs][0]+"<br>"+lec[3]+"<br>"+lec[2] ,"class='alert alert-success'" ]



        for secs in tabl[1]:
            sec=tabl[1][secs][1]
            interval[int(sec[0])-1][int(sec[1])]=[ "سكشن"+"<br>"+tabl[1][secs][0]+"<br>"+sec[3]+"<br>"+sec[2] ,"class='alert alert-info'" ]
            #interval[int(sec[0])][int(sec[1])]=[ "سكشن"+"<br>"+tabl[1][sec][0]+"<br>"+sec[3]+"<br>"+sec[2] ,"class='alert alert-success'" ]
            try:
                for labs in tabl[2]:
                    lab=tabl[2][labs][1]
                    interval[int(lab[0])-1][int(lab[1])]=[ "معمل"+"<br>"+tabl[2][labs][0]+"<br>"+lab[3]+"<br>"+lab[2] ,"class='alert alert-warning'" ]
            except:
                pass

        return render(request,"table.html",{"titles":titles,"rows":interval,"extend": "student.html" , 'table':'true'})

@login_required
def home(request):
    current_user = Students_user.objects.get(pk=request.user.id)
    context={
        'name':current_user,
        "extend": "student.html",
    }
    return render(request,"body.html",context)


@login_required
def data(request):
    current_user = Students_user.objects.get(pk=request.user.id)
    context={
        'name':current_user,
        'extend': 'student.html',
        'extend':'student.html',
        'data':'true'
    }
    return render(request , 'studentProfile.html',context)


@login_required
def grades(request):
    students = Students_user.objects.get(user=request.user)
    students = Students.objects.get(student=students)
    students = Degree.objects.filter(student=students)
    quiz = {}
    for loop in students:
        lec=LectureDegree.objects.get(lecture=loop)
        ques=lec.degr.filter(name="Quiz")
        for loop2 in ques:
            print('-'*30)
            quiz[loop.subject.subjects.name]=loop2.deg
            # print(loop2.deg)
            # print(loop.subject.subjects.name)
    # quiz =  DEG.objects.filter(name='Quiz')
    print(quiz)
    context = {
        'extend':'student.html',
        'grades':'true',
        'students':students,
        'quiz':quiz
    }
    return render(request , 'studentGrades.html',context)


@login_required
def absence(request):
    pass



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)