from database.models import *

def final_term(std,user):
    big_year=0
    smoll_term=5
    for loop in std:
        if int(loop.year)>=big_year:
            big_year=int(loop.year)
        if int(loop.term)<=smoll_term:
            smoll_term=int(loop.term)
    return (Students.objects.get( student=user,term=str(smoll_term),year=big_year ),big_year,str(smoll_term))

#####################################################################################################

def table(user):
    std=Students.objects.filter(student=user)
    std,yer,trm=final_term(std,user)
    subjects=RegisterSubject.objects.filter(students=std)
    tabl={}
    section={}
    lecture={}
    LAB={}
    for sbjct in subjects :
        lecs=Table.objects.filter(subject=sbjct.subjects,nameAction='lec',year=yer,term=trm)
        for lec in lecs:
            lecture.update( {lec.subject.name+"@"+lec.day+lec.interval:[ lec.subject.name,[lec.interval,lec.day,lec.location,lec.doctor.name]  ] })

        secs=Table.objects.filter(subject=sbjct.subjects,nameAction='sec',year=yer,term=trm)
        for sec in secs:
            section.update( {sec.subject.name+"@"+sec.day+sec.interval:[ sec.subject.name,[sec.interval,sec.day,sec.location,sec.Assistant.name]  ] })
        try:
            labs=Table.objects.filter(subject=sbjct.subjects,nameAction='lab',year=yer,term=trm)
        except:
            pass
        else:
            for lab in labs:
                LAB.update({lab.subject.name+"@"+lab.day+lab.interval: [ lab.subject.name,[lab.interval,lab.day,lab.location,lab.Assistant.name]  ] })
    return [lecture,section,LAB]


####################################################################################################################################


def RegisterSub(register):
    register.department=register.subjects.department
    for doctor in register.subjects.dector.all():
        register.current_D.add(doctor)
    for TeachindAssistanc in register.subjects.TeachindAssistanc.all():
        register.current_A.add(TeachindAssistanc)
    for lab_A in register.subjects.lab_Assistanc.all():
        register.current_L.add(lab_A)
    studs = Students.objects.filter(student=register.students.student)
    studs,A,B=final_term(studs,register.students.student.user.pk)
    register.department=studs.department
    register.level=studs.level
    register.term=studs.term
    register.save()
