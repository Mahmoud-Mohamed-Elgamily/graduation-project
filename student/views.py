from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .student import *
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

        return render(request,"table.html",{"titles":titles,"rows":interval,"extend": "basic.html"})

@login_required
def home(request):
    current_user = Students_user.objects.get(user=request.user)
    context={
        'name':current_user.name,
        "extend": "basic.html"
    }
    return render(request,"body.html",context)