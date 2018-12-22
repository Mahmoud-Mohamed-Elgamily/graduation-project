from django.contrib import admin
from .models import *
# Register your models here.

def make(modeladmin, request, queryset):
    for register in queryset:
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
        degree=Degree.objects.create(subject=register,student=register.students,midterm=0,final=0,total=0)
        lec=LectureDegree.objects.create(lecture=degree,lab=0,total=0,absence_degree=0,absence_total=0)
        if register.current_L.count():
            clum1=DEG.objects.create(name="Total",deg=0,full=50)
            clum3=DEG.objects.create(name="Practical",deg=0,full=10)
            lec.degr.add(clum1,clum3)
        else:
            clum1=DEG.objects.create(name="Total",deg=0,full=40)
            lec.degr.add(clum1)
        clum2=DEG.objects.create(name="midterm",deg=0,full=20)
        clum4=DEG.objects.create(name="Total_lec",deg=0,full=20)
        lec.degr.add(clum2,clum4)
        SectionDegree.objects.create(section=degree,total=0)
        LABDegree.objects.create(LAB=degree,total=0)
make.short_description = "make register"


class RegisterSubjectAdmin(admin.ModelAdmin):
    list_display = ['subjects', 'students',  'department', 'level', 'term', 'year', 'sucses']
    actions = [make]



admin.site.register(Doctors)
admin.site.register(DataDoctor)
admin.site.register(TeachingAssistant)
admin.site.register(DataTeachingAssistant)
admin.site.register(Subject)
admin.site.register(Students_user)
admin.site.register(Students)
admin.site.register(RegisterSubject,RegisterSubjectAdmin)
admin.site.register(StudentData)
admin.site.register(Table)
admin.site.register(Degree)
admin.site.register(DEG)
admin.site.register(Absence)
admin.site.register(LectureDegree)
admin.site.register(SectionDegree)
admin.site.register(LABDegree)
admin.site.register(User)