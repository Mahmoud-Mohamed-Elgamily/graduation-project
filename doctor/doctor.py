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
        subjectss=""
        for subjec in subject.subject.Requirement.all():
            subjectss=subjectss+str(subjec.name)+"<br>"
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

def addclums(user,title,cl,pk):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for i in range(int(cl)):
        for student in students:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            clum=DEG.objects.create(name=str(title),deg=0)
            lec.degr.add(clum)
            lec.save()
##############################################################################################################################@@@
def postclums(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        title=[["الاسم",]]
        index=[[student.students.student.name,""]]
        for clm in lec.degr.all():
            try:
                clm.deg=int(request.POST.get(str(clm.pk ) ) )
                clm.save()
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
                    title.append([clm.get_name_display(),""])
                    index.append(['<input size="1" type="text" name="'+str(clm.pk)+'" value="'+str(clm.deg)+'">',""])
                except:
                    pass
        except:
            pass
        else:
            rows.append(index)
    return title,rows


#########################################################################################################################################

def deleteclums(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    for student in students:
        try:
            DG=Degree.objects.get(subject=student,student=student.students)
            lec=LectureDegree.objects.get(lecture=DG)
            title=[["الاسم",]]
            index=[[student.students.student.name,""]]
            for clm in lec.degr.all():
                try:
                    lec.degr.remove(clm)
                    clm.delete()
                except:
                    pass
        except:
            pass
