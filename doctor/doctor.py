from database.models import *

def final_term(doctor):
    big_year=0
    small_term=5
    for loop in doctor:
        if int(loop.year)>=big_year:
            big_year=int(loop.year)
        if int(loop.term)<=small_term:
            small_term=int(loop.term)
    return ( big_year,str(small_term) )


##############################################################################################################################


def table(user):
    doc=Doctors.objects.get(user=user)
    doctor=Table.objects.filter(doctor=doc)
    yer,trm=final_term(doctor)
    subjects=Table.objects.filter( doctor=doc,nameAction='lec',term=str(trm),year=yer )
    tabl={}
    for lec in subjects :
        tabl.update( { lec.subject.name:{ "lec":[lec.interval,lec.day,lec.location,lec.subject.get_level_display() ] } } )
    return tabl



#######################################################################################################################################
def subject(user):
    doc=Doctors.objects.get(user=user)
    doctor=Table.objects.filter(doctor=doc)
    yer,trm=final_term(doctor)
    subjects=Table.objects.filter( doctor=doc,nameAction='lec',term=str(trm),year=yer )
    tabl=[]
    for subject in subjects :
        assistants=""
        for assistant in subject.subject.TeachindAssistanc.all():
            assistants=assistants+str(assistant.name)+"<br>"
        lab_Assistancs=""
        for assistant in subject.subject.lab_Assistanc.all():
            lab_Assistancs=lab_Assistancs+str(assistant.name)+"<br>"
        subjectss=RegisterSubject.objects.filter(subjects=subject.subject,term=str(trm),year=yer ).count()
        # for subjec in subject.subject.Requirement.all():
        #     subjectss=subjectss+str(subjec.name)+"<br>"
        url='<a href="'+'/doctor/subjects/'+str(subject.subject.pk)+'"><h4>'+subject.subject.name+'</h4></a>'
        tabl.append( [ [url,""],[assistants,""],[lab_Assistancs,""],[subjectss,""] ] )
    return tabl


############################################################################################################################################


def StudentSubject(p_k):
    subj=Subject.objects.get(pk=p_k)
    students=Table.objects.filter(subject=subj)
    yer,trm=final_term(students)
    students=RegisterSubject.objects.filter(subjects=subj,term=str(trm),year=yer)
    stud=[]
    for student in students:
        stud.append([ ["<h5>"+student.students.student.name+"</h5>",""] ])
    return stud,subj.name,students


######################################################################################################################################

def addclums(user,titl,cl,pk):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    titles=[]
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        for clm in lec.degr.all():
            titles.append(clm.name)
    
    
    c=1
    title=titl         
    for i in range(int(cl)):
        for student in students:
            if title not in titles :
                DG=Degree.objects.get(subject=student,student=student.students)
                lec=LectureDegree.objects.get(lecture=DG)
                clum=DEG.objects.create(name=str(title),deg=0)
                lec.degr.add(clum)
                lec.save()
        c=c+1
        title=str(titl)+str(c)
     
##############################################################################################################################@@@
def postclums(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        for clm in lec.degr.all():
            try:
                clm.update(deg=int(request.POST.get(str(clm.pk ) ) ) )
            except:
                pass

######################################################################################################################################
def Getclums(user,pk):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    title=[]
    for student in students:
        try:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            title=[["الاسم",]]
            index=[[student.students.student.name,""]]
            for clm in lec.degr.all():
                try:
                    title.append(['<input type="checkbox" name="'+clm.name+'" value='+clm.name+'> '+clm.name,""])
                    index.append(['<input size="1" type="text" name="'+str(clm.pk)+'" value="'+str(clm.deg)+'">',""])
                except:
                    pass
        except:
            pass
        else:
            rows.append(index)
    return title,rows


#########################################################################################################################################

def deleteclums(request,pk,check):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    for student in students:
        try:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            for clm in lec.degr.all():
                try:
                    if check:
                        if str(clm.name )== str(request.POST.get(clm.name) ):
                            lec.degr.remove(clm)
                            clm.delete()
                    else:
                        lec.degr.remove(clm)
                        clm.delete()
                except:
                    pass
        except:
            pass




###########################################################################################################

def addAbsence(user,cl,pk):
    deleteAbsence(user,pk,False)
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    titles=[]         
    for i in range(int(cl)):
        for student in students:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            clum=Absence.objects.create(name=i+1,check=False)
            lec.absence.add(clum)
            lec.save()


##########################################################################################################


def GetAbsence(user,pk):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    title=[]
    for student in students:
        try:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            title=[["الاسم",]]
            index=[[student.students.student.name,""]]
            for clm in lec.absence.all():
                try:
                    title.append([clm.name,""])
                    check=""
                    if clm.check:
                        check="checked"
                    index.append(['<input type="checkbox" name="'+str(clm.pk)+'" value="'+str(1)+'"'+check+'>',""])
                except:
                    pass
        except:
            pass
        else:
            rows.append(index)
    return title,rows





#########################################################################################################
def postAbsence(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        for clm in lec.absence.all():
            #try:
            if request.POST.get(str(clm.pk ) ):
                 clm.check=True
                 clm.save()
            else:
                clm.check=False
                clm.save()
            #except:
                #pass




#####################################################################################################


def deleteAbsence(user,pk,check):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for student in students:
        try:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            for clm in lec.absence.all():
                try:
                    if check:
                        clm.update(check=False)
                    else:
                        lec.absence.remove(clm)
                        clm.delete()
                except:
                    pass
        except:
            pass