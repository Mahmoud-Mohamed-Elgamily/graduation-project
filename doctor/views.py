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
        tabl=table(request.user)
        for subject in tabl:
            lec=tabl[subject]['lec']
            interval[int(lec[0])-1][int(lec[1])]=[ "محاضرة"+"<br>"+str(subject)+"<br>"+lec[3]+"<br>"+lec[2] ,"class='alert alert-success'" ]

        return render(request,"table.html",{"titles":titles,"rows":interval,'table': 'true',"extend": "basic.html"})



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
        return render(request,"table.html",{"titles":titles,"rows":rows,'subject': 'true',"extend": "basic.html"})



########################################################################
@login_required
def students(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        rows,name,reject=StudentSubject(pk)
        titles=[ [name,""] ]
        return render(request,"table.html",{"titles":titles,"rows":rows,"extend": "basic.html"})


###########################################################################

@login_required
def dgree(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        titles,rows=Getclums(request.user,pk)
        return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html"})

    if request.method =="POST":
        if request.POST.get("action")=="تسجيل":
            postclums(request,pk)
        else:
            deleteclums(request,pk)
        return redirect('doctor:dgree', pk=pk)


###################################################################################


@login_required
def AddClm(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        hidden=pk
        return render(request,"form.html",{"hidden":hidden,"extend": "basic.html"})


    if request.method =="POST":
        addclums(request.user,request.POST.get("title"),request.POST.get("colm"),request.POST.get("hidden"))
        return redirect('doctor:dgree', pk=pk)





######################################################################################################################



def student_data(request):
    return HttpResponse("not set yet")


def results(request):
    return HttpResponse("not set yet")

def exams(request):
    return HttpResponse("not set yet")

def monitor(request):
    return HttpResponse("not set yet")

def profile(request):
    return HttpResponse("not set yet")

def mail(request):
    return HttpResponse("not set yet")
