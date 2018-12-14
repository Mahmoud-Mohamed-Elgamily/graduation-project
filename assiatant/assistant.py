from database.models import *

def final_term(assistant,ass):
    big_year=0
    smoll_term=5
    for loop in assistant:
        if int(loop.year)>=big_year:
            big_year=int(loop.year)
        if int(loop.term)<=smoll_term:
            smoll_term=int(loop.term)
    return ( big_year,smoll_term)


##############################################################################################################################


def table(user):
    ass=TeachingAssistant.objects.get(user=user)
    assistant=Table.objects.filter(Assistant=ass)
    yer,trm=final_term(assistant,ass)
    subjects=Table.objects.filter( Assistant=ass,term=str(trm),year=yer )
    tabl={}
    for sec in subjects :
        tabl.update( { sec.subject.name+str(sec.day)+str(sec.interval):{ "sec":[ sec.interval,sec.day,sec.location,sec.subject.get_level_display() ,sec.get_nameAction_display(),sec.subject.name ] } } )
        print(tabl)
    return tabl
