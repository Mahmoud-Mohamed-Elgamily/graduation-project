from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .doctor import *

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
        print("ok")
        print("ok")
        print("ok")
        print("ok")
        print("ok")
        print(request)
        print(request.user)
        print("ok")
        tabl=table(request.user)
        for subject in tabl:
            lec=tabl[subject]['lec']
            interval[int(lec[0])-1][int(lec[1])]=[ "محاضرة"+"<br>"+str(subject)+"<br>"+lec[3]+"<br>"+lec[2] ,"class='alert alert-success'" ]

        return render(request,"table.html",{"titles":titles,"rows":interval,'table': 'true'})



#######################################################################################################################################



@login_required
def subjects(request):
    if request.method =="GET":
        one="اسم المادة"
        two="المعيدين"
        three="معدين المعمل"
        Four="متطلبات المادة"
        titles=[ [one,""] , [two,""] , [three,""] , [Four,""] ]

        rows=subject(request.user)
        return render(request,"table.html",{"titles":titles,"rows":rows,'subject': 'true'})


def student_data(request):
    pass
    

def results(request):
    pass

def exams(request):
    pass

def monitor(request):
    pass

def profile(request):
    pass

def mail(request):
    pass