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
def subject(user , path='/doctor/subjects/'):
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
        url='<a href="'+path+str(subject.subject.pk)+'"><h4>'+subject.subject.name+'</h4></a>'
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
                clum=DEG.objects.create(name=str(title),deg=0,full=0)
                lec.degr.add(clum)
                #lec.save()
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
        
        total_lec=0
        total=0
        for clm in lec.degr.all():
            try:
                clm.deg=int(request.POST.get(str(clm.pk ) ) )
            except :
                pass
            if clm.name != "Total_lec" and clm.name != "Practical" and clm.name != "midterm" and clm.name != "Total":
                total_lec=total_lec+clm.deg
                try:
                    clm.full=int(request.POST.get("full"+str(clm.name ) ) )
                    clm.save(update_fields=['full'])
                except:
                    pass
            elif clm.name == "Practical" or clm.name == "midterm" :
                total=total+clm.deg
            clm.save(update_fields=['deg'])
            
        sav=lec.degr.get(name="Total_lec")
        sav.deg=total_lec
        sav.save(update_fields=['deg'])
        sav=lec.degr.get(name="Total")
        sav.deg=total+total_lec
        sav.save(update_fields=['deg'])

######################################################################################################################################
def Getclums(user,pk,dis=0):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    title=[]
    for student in students:
        
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        title=[["الاسم",]]
        index=[[student.students.student.name,""]]
        for clm in lec.degr.all():
            if dis:
                disabled=""
            else:
                disabled='disabled style="background: rgb(175, 175, 180);color:black"' 
            danger=""
            titl=clm.name
            if clm.name == "Total_lec" or clm.name == "Practical" or clm.name == "midterm" or clm.name == "Total":
                titl=clm.name+" <br> "+str(clm.full)
                if clm.name == "Total_lec":
                    total_lec=0
                    for clms in lec.degr.all():
                        if clms.name != "Total_lec" and clms.name != "Practical" and clms.name != "midterm" and clms.name != "Total":
                            total_lec=total_lec+clms.full
                    if total_lec >20:
                        danger='style="background: red;color:black"'
                        titl=titl+" <br> not "+str(total_lec)
                    title.append([titl,danger])
                else:
                    title.append([titl,danger])
                danger=''
            else:
                titl=clm.name+' <br> <input size="1" type="text" name="full'+str(clm.name)+'" value="'+str(clm.full)+'" '+disabled+'>'
                title.append(['<input type="checkbox" name="'+clm.name+'" value='+clm.name+' '+disabled+'> '+titl,""])
            if clm.deg ==0:
                disabled=""
            if clm.deg > clm.full:
                danger='class="btn btn-danger"'
            if clm.name == "Total_lec" or clm.name == "Total":
                index.append([str(clm.deg),danger])
            else:
                index.append(['<input size="1" type="text" name="'+str(clm.pk)+'" value="'+str(clm.deg)+'" '+disabled+'>',danger])
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
                            sav=lec.degr.get(name="Total_lec")
                            sav.deg=sav.deg-clm.deg
                            sav.save(update_fields=['deg'])
                            sav=lec.degr.get(name="Total")
                            sav.deg=sav.deg-clm.deg
                            sav.save(update_fields=['deg'])
                            clm.delete()
                    else:
                        #lec.degr.remove(clm)
                        clm.delete()
                except:
                    pass
            if not check:
                clum1=DEG.objects.create(name="Total",deg=0,full=50)
                clum2=DEG.objects.create(name="midterm",deg=0,full=20)
                clum3=DEG.objects.create(name="Practical",deg=0,full=10)
                clum4=DEG.objects.create(name="Total_lec",deg=0,full=20)
                lec.degr.add(clum1,clum2,clum3,clum4)
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
            #lec.save()


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
                 clm.save(update_fields=['check'])
            else:
                clm.check=False
                clm.save(update_fields=['check'])
            #except:
                #pass




#####################################################################################################


def deleteAbsence(user,pk,check):
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        for clm in lec.absence.all():
            if check:
                clm.check=False
                clm.save(update_fields=['check'])
            else:
                #lec.absence.remove(clm)
                clm.delete()