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
            interval[int(lec[0])-1][int(lec[1])]=[ "محاضرة "+str(subject)+"<br>"+lec[3]+"<br>"+'قاعة '+lec[2] ,"class='alert alert-success'" ]

        return render(request,"table.html",{"titles":titles,"rows":interval,'table': 'true',"extend": "basic.html"})



#######################################################################################################################################



@login_required
def subjects(request):
    if request.method =="GET":
        one="اسم المادة"
        two="المعيدين"
        three="معدين المعمل"
        Four="عدد طلاب المادة"
        titles=[ [one,""] , [two,""] , [three,""] , [Four,""] ]

        rows=subject(request.user,1)
        return render(request,"table.html",{"titles":titles,"rows":rows,'subject': 'true',"extend": "basic.html"})

#####################################################################################################################
def details(request,pk):
    subject_pk=Subject.objects.get(pk=pk )
    titles=[ ['<h1>'+subject_pk.name+'</h1>','colspan="2"'] ]
    
    rows=[ [ ["Specialization",""] ,[subject_pk.get_Specialization_display(),'']  ],[ ["department",""] ,[subject_pk.get_department_display(),''] ],[ ["no_hours",""] ,[subject_pk.no_hours,''] ],[ ["Optional",""] ,[subject_pk.get_Optional_display(),''] ],[ ["level",""] ,[subject_pk.get_level_display(),''] ]]
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
        elif request.POST.get("action")=="مسح المحدد":
            deleteclums(request,pk,True)
        elif request.POST.get("action")=="اضافة عمود":
            return redirect('doctor:addclm',pk=pk)
        elif request.POST.get("action")=="تعديل":
            titles,rows=Getclums(request.user,pk,1)
            return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html"})

        else:
            deleteclums(request,pk,False)
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



###################################################################################


@login_required
def addAbsences(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        hidden=pk
        return render(request,"absence.html",{"hidden":hidden,"extend": "basic.html"})


    if request.method =="POST":
        addAbsence(request.user,request.POST.get("colm"),request.POST.get("hidden"))
        return redirect('doctor:absence', pk=pk)
        




###########################################################################

@login_required
def Absences(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        titles,rows=GetAbsence(request.user,pk)
        return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html"})

    if request.method =="POST":
        if request.POST.get("action")=="تسجيل":
            postAbsence(request,pk)
        elif request.POST.get("action")=="مسح المحدد":
            deleteAbsence(request.user,pk,True)
        elif request.POST.get("action")=="اضافة عمود":
            return redirect('doctor:addabsence',pk=pk)
        else:
            deleteAbsence(request.user,pk,False)
        return redirect('doctor:absence', pk=pk)



######################################################################################################################



def student_data(request):
    return HttpResponse("not set yet")


def results(request):
    if request.method =="GET":
        one="اسم المادة"
        two="المعيدين"
        three="معيدين المعمل"
        Four="عدد طلاب المادة"
        titles=[ [one,""] , [two,""] , [three,""] , [Four,""] ]

        rows=subject(request.user , '')
        return render(request,"table.html",{"titles":titles,"rows":rows,'results': 'true',"extend": "basic.html"})


def absence(request):
    if request.method =="GET":
        one="اسم المادة"
        two="المعيدين"
        three="معيدين المعمل"
        Four="عدد طلاب المادة"
        titles=[ [one,""] , [two,""] , [three,""] , [Four,""] ]

        rows=subject(request.user , '')
        return render(request,"table.html",{"titles":titles,"rows":rows,'absence': 'true',"extend": "basic.html"})


def monitor(request):
    return HttpResponse("not set yet")

def profile(request):
    return HttpResponse("not set yet")

def mail(request):
    return HttpResponse("not set yet")
