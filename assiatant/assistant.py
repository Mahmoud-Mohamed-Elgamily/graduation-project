from database.models import *
from django.db.models import Q
from itertools import islice

def final_term(assistant):
    big_year=0
    small_term=5
    for loop in assistant:
        if int(loop.year)>=big_year:
            big_year=int(loop.year)
        if int(loop.term)<=small_term:
            small_term=int(loop.term)
    return ( big_year,str(small_term) )


##############################################################################################################################


def table(user):
    ass=TeachingAssistant.objects.get(user=user)
    assistant=Table.objects.filter(Assistant=ass)
    yer,trm=final_term(assistant)
    subjects=Table.objects.filter( Assistant=ass,term=str(trm),year=yer )
    tabl={}
    for sec in subjects :
        tabl.update( { sec.subject.name+str(sec.day)+str(sec.interval):{ "sec":[ sec.interval,sec.day,sec.location,sec.subject.get_level_display() ,sec.get_nameAction_display(),sec.subject.name ] } } )
    return tabl
##############################################################################################################################


def depart_table(user):
    ass=TeachingAssistant.objects.get(user=user)
    assistant=Table.objects.filter(department=ass.department)
    yer,trm=final_term(assistant)
    subjects=Table.objects.filter( department=ass.department,term=str(trm),year=yer )
    section={}
    lecture={}
    LAB={}
    for sbjct in subjects :
        if sbjct.nameAction =='lec':
            lecture.update( {sbjct.subject.name+"@"+sbjct.day+sbjct.interval:[ sbjct.subject.name,[sbjct.interval,sbjct.day,sbjct.location,sbjct.doctor.name]  ] })

        elif sbjct.nameAction =='sec':
            section.update( {sbjct.subject.name+"@"+sbjct.day+sbjct.interval:[ sbjct.subject.name,[sbjct.interval,sbjct.day,sbjct.location,sbjct.Assistant.name]  ] })
        elif sbjct.nameAction =='lab':
            LAB.update({sbjct.subject.name+"@"+sbjct.day+sbjct.interval: [ sbjct.subject.name,[sbjct.interval,sbjct.day,sbjct.location,sbjct.Assistant.name]  ] })
    return [lecture,section,LAB]
###################################################################################################################################################################################
def subject(user , subjects=0,yer=0,trm=0):
    if not subjects :
        ass=TeachingAssistant.objects.get(user=user)
        subjects=Table.objects.filter(Assistant=ass)
        yer,trm=final_term(subjects)
        subjects=Table.objects.filter( Q(Assistant=ass,nameAction='sec',term=str(trm),year=yer)|Q(Assistant=ass,nameAction='lab',term=str(trm),year=yer) )
        return subjects,yer,trm
    tabl=[]
    for subject in subjects :
        cheack=True
        url1='<a href="details/'+str(subject.subject.pk)+'"><h4>'+str(subject.subject.name)+'</h4></a>'
        for index in tabl:
            if [url1,""] in index:
                cheack=False
        if cheack:
            doctors=""
            for doctor in subject.subject.dector.all():
                doctors=doctors+str(doctor.name)+"<br>"
            sec_Assistancs=""
            for assistant in subject.subject.TeachindAssistanc.all():
                sec_Assistancs=sec_Assistancs+str(assistant.name)+"<br>"
            lab_Assistancs=""
            for assistant in subject.subject.lab_Assistanc.all():
                lab_Assistancs=lab_Assistancs+str(assistant.name)+"<br>"
            subjectss=RegisterSubject.objects.filter(subjects=subject.subject,term=str(trm),year=yer ).count()
            # for subjec in subject.subject.Requirement.all():
            #     subjectss=subjectss+str(subjec.name)+"<br>"

            

            url='<a href="'+str(subject.subject.pk)+'"><h4>'+str(subjectss)+'</h4></a>'
            tabl.append( [ [url1,""],[doctors,""],[sec_Assistancs,""],[lab_Assistancs,""],[url,""] ] )
    return tabl


###########################################################################################################################################
def StudentSubject(p_k):
    subj=Subject.objects.get(pk=p_k)
    students=Table.objects.filter(subject=subj)
    yer,trm=final_term(students)
    students=RegisterSubject.objects.filter(subjects=subj,term=str(trm),year=yer)
    stud=[]
    for student in students:
        stud.append([ ["<h5>"+student.students.student.name+"</h5>",""] ])
    return stud,subj.name,students



    ################################################################################################################
def Getclums(user,pk,dis=0):
    ass=TeachingAssistant.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    rows=[]
    title=[]
    script=""
    for student in students:

        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        if not sec.finsh:

            script='"تسليم.الكشف" '
        else:
            script='"تم.تسليم.الكشف" '+'disabled'
        title=[["الاسم",]]
        index=[[student.students.student.name,""]]
        full=0
        for clm in sec.degr.order_by('-pk').reverse():
            if dis and not sec.finsh:
                disabled=""
            else:
                disabled='disabled style="background: rgb(175, 175, 180);color:black"'
            danger=""
            
            titl=clm.name+' <br> <input size="1" type="text" name="full'+str(clm.name)+'" value="'+str(clm.full)+'" '+disabled+'>'
            title.append(['<input type="checkbox" name="'+clm.name+'" value='+clm.name+' '+disabled+'> '+titl,""])
            full=full+clm.full
            if clm.deg ==0 and not sec.finsh:
                disabled=""
            elif clm.deg > clm.full:
                danger='class="btn btn-danger"'
            if clm.name == "Absence":
                index.append([int(clm.deg),""])
            else:
                index.append(['<input size="1" type="text" name="'+str(clm.pk)+'" value="'+str(clm.deg)+'" '+disabled+'>',danger])
        index.append([sec.total,""])    
        rows.append(index)
        title.append(["total_sec<br>"+str(sec.full_degree),""])
        sec.full_degree=full
        sec.save(update_fields=['full_degree'])
        address=student.subjects.name
    return title,rows,address,script
#############################################################################################################################
def addclums(user,titl,cl,pk):
    ass=TeachingAssistant.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    titles=[]
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        for clm in sec.degr.all():
            titles.append(clm.name)


    c=1
    title=titl
    for i in range(int(cl)):
        for student in students:
            if title not in titles :
                DG=Degree.objects.get(subject=student,student=student.students)
                sec=SectionDegree.objects.get(section=DG)
                clum=DEG.objects.create(name=str(title),deg=0,full=0)
                sec.degr.add(clum)
                #sec.save()
        c=c+1
        title=str(titl)+str(c)

##############################################################################################################################@@@
def postclums(request,pk):
    ass=TeachingAssistant.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        if not sec.finsh:
            total_sec=0
            full=0
            for clm in sec.degr.all():
                try:
                    clm.deg=int(request.POST.get(str(clm.pk ) ) )
                    clm.save(update_fields=['deg'])
                except :
                    pass
                
                try:
                    clm.full=int(request.POST.get("full"+str(clm.name ) ) )
                    clm.save(update_fields=['full'])
                    full=full+clm.full
                except:
                    pass

                if clm.name == "Absence":
                    clm.deg=int( (sec.absence_degree*clm.full)/sec.absence_total )
                    clm.save(update_fields=['deg'])
                
                total_sec=total_sec+clm.deg
                
            
            sec.total=total_sec
            sec.save(update_fields=['total'])
            sec.full_degree=full
            sec.save(update_fields=['full_degree'])

######################################################################################################################################
def finsh(request,pk):
    ass=TeachingAssistant.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        if not sec.finsh:
            sec.finsh=True
            sec.save(update_fields=['finsh']) 







################################################################################################################################################
def deleteclums(request,pk,check):
    ass=TeachingAssistant.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    rows=[]
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        for clm in sec.degr.all():
            try:
                if check:
                    if str(clm.name )== str(request.POST.get(clm.name) ):
                        sec.total=sec.total-clm.deg
                        sec.save(update_fields=['total'])
                        clm.delete()
                else:
                    
                    clm.delete()
            except:
                pass
        if not check:
            sec.total=0
            sec.save(update_fields=['total'])



###########################################################################################################

def addAbsence(user,cl,pk):
    deleteAbsence(user,pk,False)
    ass=TeachingAssistant.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    index=[]
    rang=students.count()
    for count in range(rang):
        for i in range(int(cl)):
            index.append(Absence(name=i+1,check=False))
    #if rang*int(cl) >100
    batch_size = len(index)
    batch = list(islice(index, batch_size))
    Absence.objects.bulk_create(batch, batch_size)

    firist_pk=(Absence.objects.latest('id').pk-(rang*int(cl) ) )+1
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        for i in range(int(cl)):
            sec.absence.add(firist_pk)
            firist_pk=firist_pk+1
        sec.absence_total=int(cl)
        sec.save(update_fields=['absence_total'])

##########################################################################################################


def GetAbsence(user,pk,dis=0):
    ass=TeachingAssistant.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    rows=[]
    title=[]
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        title=[["الاسم",]]
        index=[[student.students.student.name,""]]
        for clm in sec.absence.order_by('-pk').reverse():
            title.append([clm.name,""])
            disabled=""
            check=""
            if clm.check:
                check="checked"
                if dis:
                    disabled="disabled"
            index.append(['<input type="checkbox" name="'+str(clm.pk)+'" value="'+str(1)+'"'+check+' '+disabled+'>',""])


        index.append([sec.absence_degree,""])
        rows.append(index)
    title.append(["total",""])
    address=student.subjects.name
    return title,rows,address





#########################################################################################################
def postAbsence(request,pk):
    ass=TeachingAssistant.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        total=0
        for clm in sec.absence.all():
            #try:
            if request.POST.get(str(clm.pk ) ):
                 clm.check=True
                 total=total+1
                 clm.save(update_fields=['check'])
            else:
                clm.check=False
                clm.save(update_fields=['check'])
        sec.absence_degree=total
        sec.save(update_fields=['absence_degree'])
            #except:
                #pass




#####################################################################################################


def deleteAbsence(user,pk,check):
    ass=TeachingAssistant.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(Assistant=ass))
    students=RegisterSubject.objects.filter(current_A=ass,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        for clm in sec.absence.all():
            if check:
                clm.check=False
                clm.save(update_fields=['check'])
            else:
                #sec.absence.remove(clm)
                clm.delete()
        sec.absence_degree=0
        sec.save(update_fields=['absence_degree'])
