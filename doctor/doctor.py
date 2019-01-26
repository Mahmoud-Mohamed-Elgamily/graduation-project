from database.models import *
from itertools import islice

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
def Necessaryclums(request,pk,student,lec,get=0):
    cheack=False
    try:
        lec.degr.get(name="Total_lec")
    except:
        cheack=True
        lec.degr.add( DEG.objects.create(name="Total_lec",deg=0,full=20,show=False) )
    try:
        lec.degr.get(name="midterm")
    except:
        lec.degr.add(DEG.objects.create(name="midterm",deg=0,full=20,show=False))
    if student.current_L.count():
        try:
            lec.degr.get(name="Total")
        except:
            cheack=True
            lec.degr.add(DEG.objects.create(name="Total",deg=0,full=50,show=False))
        try:
            lec.degr.get(name="Practical")
        except:
            lec.degr.add(DEG.objects.create(name="Practical",deg=0,full=10,show=False))
            
    else:
        try:
            lec.degr.get(name="Total")
        except:
            cheack=True
            lec.degr.add(DEG.objects.create(name="Total",deg=0,full=40,show=False))
    
    if cheack and get:
        postclums(request,pk)

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







##############################################################################################################################


def depart_table(user):
    doc=Doctors.objects.get(user=user)
    subjects=Table.objects.filter(department=doc.department)
    yer,trm=final_term(subjects)
    subjects=subjects=Table.objects.filter( department=doc.department,term=str(trm),year=yer )
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



#######################################################################################################################################
def subject(user , subjects=0,yer=0,trm=0):
    if not subjects :
        doc=Doctors.objects.get(user=user)
        doctor=Table.objects.filter(doctor=doc)
        yer,trm=final_term(doctor)
        subjects=Table.objects.filter( doctor=doc,nameAction='lec',term=str(trm),year=yer )
        return subjects,yer,trm
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

        url1='<a href="details/'+str(subject.subject.pk)+'"><h4>'+str(subject.subject.name)+'</h4></a>'

        url='<a href="'+str(subject.subject.pk)+'"><h4>'+str(subjectss)+'</h4></a>'
        tabl.append( [ [url1,""],[assistants,""],[lab_Assistancs,""],[url,""] ] )
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
                clum=DEG.objects.create(name=str(title),deg=0,full=0,show=False)
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
        Necessaryclums(request,pk,student,lec,False)
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
def definsh(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        sec=SectionDegree.objects.get(section=DG)
        if sec.finsh:
            sec.finsh=False
            sec.save(update_fields=['finsh'])
######################################################################################################################################
def Getclums(request,pk,dis=0):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    title=[]
    script=""
    for student in students:

        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        sec=SectionDegree.objects.get(section=DG)
        Necessaryclums(request,pk,student,lec,True)
        if sec.finsh:

            script='"اعاة.درجات.السكشن" '
        else:
            script='"لم.تكتمل.درجات.السكشن" '+'disabled'
        title=[["الاسم",]]
        index=[[student.students.student.name,""]]
        for clm in lec.degr.order_by('-pk').reverse():
            show=""
            if clm.show:
                show="ظاهر"
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
                    for clms in lec.degr.order_by('-pk').reverse():
                        if clms.name != "Total_lec" and clms.name != "Practical" and clms.name != "midterm" and clms.name != "Total":
                            total_lec=total_lec+clms.full
                    if total_lec != 20 :
                        danger='style="background: red;color:black"'
                        titl=titl+" <br> not "+str(total_lec)
                    title.append(['<input type="checkbox" name="'+clm.name+'" value='+clm.name+' '+disabled+'> '+titl+"<br>"+show,danger])
                else:
                    title.append(['<input type="checkbox" name="'+clm.name+'" value='+clm.name+' '+disabled+'> '+titl+"<br>"+show,danger])
                danger=''
            else:
                titl=clm.name+' <br> <input size="1" type="text" name="full'+str(clm.name)+'" value="'+str(clm.full)+'" '+disabled+'>'
                title.append(['<input type="checkbox" name="'+clm.name+'" value='+clm.name+' '+disabled+'> '+titl+"<br>"+show,""])
            if clm.deg ==0:
                disabled=""
            if clm.deg > clm.full:
                danger='class="btn btn-danger"'
            if clm.name == "Total_lec" or clm.name == "Total":
                index.append([str(clm.deg),danger])
            elif clm.name == "Absence":
                clm.deg=((lec.absence_degree*clm.full)/lec.absence_total)
                clm.save(update_fields=['deg'])
                index.append([int(clm.deg),""])
            elif clm.name == "Section":
                sec=SectionDegree.objects.get(section=DG)
                if sec.finsh:
                    clm.deg=((sec.total*clm.full)/sec.full_degree)
                    clm.save(update_fields=['deg'])
                    if clm.deg > clm.full:
                        danger='class="btn btn-danger"'
                    index.append([int(clm.deg),danger])
                else:
                    clm.deg=0
                    clm.save(update_fields=['deg'])
                    index.append(["not finshed",""])
            else:
                index.append(['<input size="1" type="text" name="'+str(clm.pk)+'" value="'+str(clm.deg)+'" '+disabled+'>',danger])
        rows.append(index)
        address=student.subjects.name
    
    return title,rows,address,script


#########################################################################################################################################

def deleteclums(request,pk,check):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    for student in students:
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
            if student.current_L.count():
                clum1=DEG.objects.create(name="Total",deg=0,full=50,show=False)
                clum3=DEG.objects.create(name="Practical",deg=0,full=10,show=False)
                lec.degr.add(clum1,clum3)
            else:
                clum1=DEG.objects.create(name="Total",deg=0,full=40,show=False)
                lec.degr.add(clum1)
            clum2=DEG.objects.create(name="midterm",deg=0,full=20,show=False)
            clum4=DEG.objects.create(name="Total_lec",deg=0,full=20,show=False)
            lec.degr.add(clum2,clum4)

#########################################################################################################################################

def show(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    rows=[]
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        for clm in lec.degr.all():
            try:
            
                if str(clm.name )== str(request.POST.get(clm.name) ):
                    clm.show=True
                    clm.save(update_fields=['show'])
                
            except:
                pass
        





###########################################################################################################

def addAbsence(user,cl,pk):
    deleteAbsence(user,pk,False)
    doc=Doctors.objects.get(user=user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
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
        lec=LectureDegree.objects.get(lecture=DG)
        for i in range(int(cl)):
            lec.absence.add(firist_pk)
            firist_pk=firist_pk+1
        lec.absence_total=int(cl)
        lec.save(update_fields=['absence_total'])

##########################################################################################################


def GetAbsence(user,pk,dis=0):
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
        for clm in lec.absence.order_by('-pk').reverse():
            title.append([clm.name,""])
            disabled=""
            check=""
            if clm.check:
                check="checked"
                if dis:
                    disabled="disabled"
            index.append(['<input type="checkbox" name="'+str(clm.pk)+'" value="'+str(1)+'"'+check+' '+disabled+'>',""])


        index.append([lec.absence_degree,""])
        rows.append(index)
    title.append(["total",""])
    address=student.subjects.name
    return title,rows,address





#########################################################################################################
def postAbsence(request,pk):
    doc=Doctors.objects.get(user=request.user)
    yer,trm=final_term(Table.objects.filter(doctor=doc))
    students=RegisterSubject.objects.filter(current_D=doc,subjects=pk,term=str(trm),year=yer)
    for student in students:
        DG=Degree.objects.get(subject=student,student=student.students)
        lec=LectureDegree.objects.get(lecture=DG)
        total=0
        for clm in lec.absence.all():
            #try:
            if request.POST.get(str(clm.pk ) ):
                 clm.check=True
                 total=total+1
                 clm.save(update_fields=['check'])
            else:
                clm.check=False
                clm.save(update_fields=['check'])
        lec.absence_degree=total
        lec.save(update_fields=['absence_degree'])
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
        lec.absence_degree=0
        lec.save(update_fields=['absence_degree'])

