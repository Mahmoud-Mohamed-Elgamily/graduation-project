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
        subjects,yer,trm=subject(request.user)
        for subject1 in tabl:
            lec=tabl[subject1]['lec']
            interval[int(lec[0])-1][int(lec[1])]=[ "محاضرة "+str(subject1)+"<br>"+lec[3]+"<br>"+'قاعة '+lec[2] ,"class='alert alert-success'" ]

        return render(request,"table.html",{"titles":titles,"rows":interval,'table': 'true',"extend": "basic.html","subjects":subjects})
################################################################################################################################################################
@login_required
def depart_tbl(request):
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
        tabl=depart_table(request.user.pk)
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
        subjects,yer,trm=subject(request.user)
        return render(request,"table.html",{"titles":titles,"rows":interval,"extend": "basic.html","subjects":subjects})


#######################################################################################################################################



@login_required
def subjects(request):
    if request.method =="GET":
        one="اسم المادة"
        two="المعيدين"
        three="معيدين المعمل"
        Four="عدد طلاب المادة"
        titles=[ [one,""] , [two,""] , [three,""] , [Four,""] ]
        subjects,yer,trm=subject(request.user)
        rows=subject(request.user,subjects,yer,trm)
        return render(request,"table.html",{"titles":titles,"rows":rows,'subject': 'true',"extend": "basic.html","subjects":subjects})

#####################################################################################################################
@login_required
def details(request,pk):
    subject_pk=Subject.objects.get(pk=pk )
    titles=[ ['<h1>'+subject_pk.name+'</h1>','colspan="2"'] ]

    rows=[ [ ["Specialization",""] ,[subject_pk.get_Specialization_display(),'']  ],[ ["department",""] ,[subject_pk.get_department_display(),''] ],[ ["no_hours",""] ,[subject_pk.no_hours,''] ],[ ["Optional",""] ,[subject_pk.get_Optional_display(),''] ],[ ["level",""] ,[subject_pk.get_level_display(),''] ]]
    subjects,yer,trm=subject(request.user)
    return render(request,"table.html",{"titles":titles,"rows":rows,'subject': 'true',"extend": "basic.html","subjects":subjects})

########################################################################
@login_required
def students(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        subjects,yer,trm=subject(request.user)
        rows,name,reject=StudentSubject(pk)
        titles=[ ["<h3>"+name+"</h3>",""] ]
        return render(request,"table.html",{"titles":titles,"rows":rows,"extend": "basic.html","subjects":subjects})


###########################################################################

@login_required
def dgree(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        titles,rows,address,script=Getclums(request,pk)
        subjects,yer,trm=subject(request.user)
        return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html","address":address,"script":script,"subjects":subjects})

    if request.method =="POST":
        if request.POST.get("action")=="تسجيل":
            postclums(request,pk)
            Getclums(request,pk)#fixed only
        elif request.POST.get("action")=="مسح المحدد":
            deleteclums(request,pk,True)
        elif request.POST.get("action")=="اضافة عمود":
            return redirect('doctor:addclm',pk=pk)
        elif request.POST.get("action")=="تعديل":
            titles,rows,address,script=Getclums(request,pk,1)
            subjects,yer,trm=subject(request.user)
            return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html","adress":address,"script":script,"subjects":subjects})
        elif request.POST.get("action")=='"اعاة.درجات.السكشن"':
            definsh(request,pk)
            return redirect('doctor:dgree', pk=pk)
        elif request.POST.get("action")=='اعلان.المحدد.للطلبة':
            show(request,pk)
            return redirect('doctor:dgree', pk=pk)
        else:
            deleteclums(request,pk,False)
        return redirect('doctor:dgree', pk=pk)


###################################################################################


@login_required
def AddClm(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        hidden=pk
        subjects,yer,trm=subject(request.user)
        return render(request,"form.html",{"hidden":hidden,"extend": "basic.html","subjects":subjects})


    if request.method =="POST":
        addclums(request.user,request.POST.get("title"),request.POST.get("colm"),request.POST.get("hidden"))
        return redirect('doctor:dgree', pk=pk)



###################################################################################


@login_required
def addAbsences(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        hidden=pk
        subjects,yer,trm=subject(request.user)
        return render(request,"absence.html",{"hidden":hidden,"extend": "basic.html","subjects":subjects})


    if request.method =="POST":
        addAbsence(request.user,request.POST.get("colm"),request.POST.get("hidden"))
        return redirect('doctor:absence', pk=pk)





###########################################################################

@login_required
def Absences(request,pk):#               دي انا سايبها لبعدين لان السكيرتي هنا مش قد كده
    if request.method =="GET":
        titles,rows,address=GetAbsence(request.user,pk)
        print("ok ")
        print("ok ")
        print(address)
        subjects,yer,trm=subject(request.user)
        return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html","address":address,"subjects":subjects})

    if request.method =="POST":
        if request.POST.get("action")=="تسجيل":
            postAbsence(request,pk)
        elif request.POST.get("action")=="مسح المحدد":
            deleteAbsence(request.user,pk,True)
        elif request.POST.get("action")=="اضافة عمود":
            return redirect('doctor:addabsence',pk=pk)
        elif request.POST.get("action")== "تعديل" :
            titles,rows,address=GetAbsence(request.user,pk,0)
            subjects,yer,trm=subject(request.user)
            return render(request,"table.html",{"titles":titles,"rows":rows,"register":1,"id":pk,"extend": "basic.html","address":address,"subjects":subjects})

        else:
            deleteAbsence(request.user,pk,False)
        return redirect('doctor:absence', pk=pk)



######################################################################################################################


@login_required
def home(request):
    current_user = Doctors.objects.get(user=request.user)
    subjects,yer,trm=subject(request.user)
    context={
        'name':'د/ '+current_user.name,
        "subjects":subjects,
        "extend": "basic.html"
    }
    return render(request,"body.html",context)

#################################################################################################
def student_data(request):
    return HttpResponse("not set yet")



def monitor(request):
    return HttpResponse("not set yet")

def profile(request):
    return HttpResponse("not set yet")

def mail(request):
    return HttpResponse("not set yet")
