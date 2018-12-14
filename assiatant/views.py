from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .assistant import *

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
        for subject in tabl:
            lec=tabl[subject]['sec']
            interval[int(lec[0])-1][int(lec[1])]=[ lec[4]+"<br>"+str(lec[5])+"<br>"+lec[3]+"<br>"+lec[2] ,"class='alert alert-success'" ]

        return render(request,"table.html",{"titles":titles,"rows":interval})
