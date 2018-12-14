from database.models import *

def final_term(doctor):
    big_year=0
    smoll_term=5
    for loop in doctor:
        if int(loop.year)>=big_year:
            big_year=int(loop.year)
        if int(loop.term)<=smoll_term:
            smoll_term=int(loop.term)
    return ( big_year,smoll_term )


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
    print("ok")
    print("ok")
    print("ok")
    print("ok")
    print("ok")
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
        for subject in subject.subject.Requirement.all():
            subjectss=subjectss+str(subject.name)+"<br>"
        tabl.append( [ [subject.subject.name,""],[assistants,""],[lab_Assistancs,""],[subjectss,""] ] )
    return tabl
