from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
import random
# Create your views here.
@login_required
def quis(request):
    m=""
    s=""
    if request.method =="GET":
        if str(request.user.username)=="a":
            student=students.objects.all()
            fin=[]
            time=[]
            don=[]
            list=[]
            for stud in student:
                test=True
                i=0
                list_loop=[]
                ips=students.objects.filter(ip=stud.ip)
                for loop in ips:
                    i=i+1
                if i > 1 :
                    for lists in list :
                        if loop.name in lists :
                            test=False
                    if test :
                        for loop in ips:
                            if loop.ip :
                                list_loop.append(loop.name)
                        if  len(list_loop) >0:
                            list.append(list_loop)
                if stud.finsh:
                    fin.append(stud.code)
                elif stud.no_of_enter == 0 :
                    don.append(stud.code)
                else :
                    time.append(stud.code)
            finsh=students.objects.filter(code__in=fin).distinct()
            time_out=students.objects.filter(code__in=time).distinct()
            dont=students.objects.filter(code__in=don).distinct()
            return render(request,"quizes/table.html",{"finsh":finsh,"time_out":time_out,"dont":dont,"list":list})
        user=Students_user.objects.get(user=request.user)
        student=students.objects.get(user=user)
        if student.finsh:
            return render(request,"quizes/result.html",{"Degree":"result="+str(student.Degree),"name":student.name,"code":student.code})
        if student.no_of_enter == 0:
            #return render(request,"quizes/result.html",{"Degree":"result="+"الامتحان انتهي","name":student.name,"code":student.code})
            m="00"
            s="00"
            student.last_time=str(datetime.now()).split(" ")[1].split(".")[0]
            student.save()
            que=questions.objects.all()
            l=[]
            for question in que:
                l.append(question.questions)
            choose=random.sample(l,5)
            for loop in choose:
                que=questions.objects.get(questions=loop)
                student.questions.add(que)
            student.save()
        else:
            #return render(request,"quizes/result.html",{"Degree":"Time out","name":student.name,"code":student.code})
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(str(datetime.now()).split(" ")[1].split(".")[0], FMT) - datetime.strptime(student.last_time, FMT)
            if int(str(tdelta).split(":")[0]) >0:
                return render(request,"quizes/result.html",{"Degree":"Time out","name":student.name,"code":student.code})
            if int(str(tdelta).split(":")[1]) >=3:
                return render(request,"quizes/result.html",{"Degree":"Time out","name":student.name,"code":student.code})
            m=str(tdelta).split(":")[1]
            s=str(tdelta).split(":")[2]
        student.no_of_enter=student.no_of_enter+1
        #student.ip=str(request.META['HTTP_X_REAL_IP'])
        student.save()
        quies=[]
        for loop in student.questions.all():
            quies.append(loop)
        que=questions.objects.filter(questions__in=quies).distinct()
        return render(request,"quizes/exam.html",{"que":que,"m":m,"s":s})

    if request.method=='POST':
        user=Students_user.objects.get(user=request.user)
        student=students.objects.get(user=user)
        if student.finsh:
            return render(request,"quizes/result.html",{"Degree":"result="+str(student.Degree),"name":student.name,"code":student.code})
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(str(datetime.now()).split(" ")[1].split(".")[0], FMT) - datetime.strptime(student.last_time, FMT)
        if int(str(tdelta).split(":")[0]) >0:
            return redirect('quis:quies')
        if int(str(tdelta).split(":")[1]) >3:
            return redirect('quis:quies')
        student.Degree=0
        student.save()
        que=student.questions.all()
        choose="&"
        degr=0
        print(que)
        for loop in que:
            choose=choose+str(loop.pk)+">"+str(request.POST.get(str(loop.pk)))+","
            if str(loop.correct) == str(request.POST.get(str(loop.pk))):
                degr=degr+1
            student.Degree=degr
            student.finsh=True
            student.time=str(tdelta)+choose
            student.save()
        return render(request,"quizes/result.html",{"Degree":"result="+str(degr),"name":student.name,"code":student.code})

    else:
        return HttpResponse("اوعي تفكر نفسك شاطر")




@login_required
def studen(request,cod):
    if request.method =="GET":
        if str(request.user.username)=="a":
            student=students.objects.get(code=cod)
            quies=[]
            for loop in student.questions.all():
                quies.append(loop)
            que=questions.objects.filter(questions__in=quies).distinct()
            all=str(student.time).split("&")
            time=str(all[0])
            answer=str(all[1]).split(",")
            answer.remove("")
            dic={}
            for loop in que:
                for answers in answer:
                    ans=str(answers).split(">")
                    print(ans)
                    if int(ans[0])==loop.pk:
                        dic.update({str(loop.questions)+"{"+str(ans[1])+":"+str(loop.correct)+"}":[loop.A,loop.B,loop.C]})
            print(dic)
            return render(request,"quizes/rebort.html",{"que":dic,"m":time,"stu":student})
        else:
            return HttpResponse("اوعي تفكر نفسك شاطر")
    else:
        return HttpResponse("اوعي تفكر نفسك شاطر")






# if student.last_time:
#     time = str(datetime.now())[11:19]
#     FMT = '%H:%M:%S'
#     tdelta = datetime.strptime(time, FMT) - datetime.strptime(student.last_time, FMT)
#     hours=int(str(tdelta)[:2])
#     if hours > 0:
