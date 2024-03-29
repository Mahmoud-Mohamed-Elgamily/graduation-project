import sys
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



class User(AbstractUser):
    is_student   = models.BooleanField(default=False)
    is_teacher   = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)

User=get_user_model()
# Create your models here.
Levels=(
(str(1),'المستوي الاول'),
(str(2),'المستوي الثاني'),
(str(3),'المستوي الثالث'),
(str(4),'المستوي الرابع'),
)

Departments=(
(str(0),"اعدادي"),
(str(1),"مدني"),
(str(2),"اتصلات"),
(str(3),"عمارة"),
(str(4),"مشترك"),
)

GENDER_CHOICES = (
    ('ذكر', 'ذكر'),
    ('أنثي', 'أنثي'),
)
Terms=(
(str(1),'الترم الاول'),
(str(2),'الترم الصيفي'),
(str(3),'الترم الثاني'),
)


Action=(
('lec','lecture'),
('sec','section'),
('lab','lab'),
)

specialization=(
(str(1),'ثقافي'),
(str(2),'معهد'),
(str(3),'الشعبة'),
(str(4),'التخصص'),
)



optional=(
(str(1),'اجباري'),
(str(2),'اختياري'),
)


day=(
(str(1),'السبت'),
(str(2),'الاحد'),
(str(3),'الاثنين'),
(str(4),'الثلاثاء'),
(str(5),'الاربعاء'),
(str(6),'الخميس'),
)



interval=(
(str(1),'الاولي'),
(str(2),'الثانية'),
(str(3),'الثالثة'),
(str(4),'الرابعة'),
)





# NameDeg=(
# (str(1),'Midterm'),
# (str(2),'Quiz'),
# (str(3),'Report'),
# (str(4),'Absence'),
# (str(5),'Section'),
# (str(6),'LAB'),
# )




def final_term(std,user):
    big_year=0
    smoll_term=5
    for loop in std:
        if int(loop.year)>=big_year:
            big_year=int(loop.year)
        if int(loop.term)<=smoll_term:
            smoll_term=int(loop.term)
    return (Students.objects.get( student=user,term=str(smoll_term),year=big_year ),big_year,str(smoll_term))




class Doctors(models.Model):
    # Relations
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    # Variables
    department = models.CharField(max_length=100,choices=Departments)
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name



############################################################################################################################



class DataDoctor(models.Model):
    # Relations
    doctor = models.OneToOneField(Doctors,on_delete=models.CASCADE,unique=True)
    # Variables
    doc_code = models.PositiveIntegerField(unique=True)
    place = models.CharField(max_length=400)
    def __str__(self):
        return self.doctor.name


############################################################################################################################


class TeachingAssistant(models.Model):
    # Relations
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    # Variables
    department = models.CharField(max_length=100,choices=Departments)
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name




############################################################################################################################


class DataTeachingAssistant(models.Model):
    # Relations
    ta = models.OneToOneField(TeachingAssistant,on_delete=models.CASCADE)
    # Variables
    ta_code = models.PositiveIntegerField(unique=True)
    place = models.CharField(max_length=400)
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.ta.name



############################################################################################################################



class Students_user(models.Model):
    # Relations
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    # Variables
    name = models.CharField(max_length=100,unique=True)

    class Meta:
        unique_together = ( "user","name")

    def __str__(self):
        return self.name



############################################################################################################################


class Students(models.Model):
    # Relations
    student = models.ForeignKey(Students_user,on_delete=models.CASCADE)
    # Variables
    department = models.CharField(max_length=100,choices=Departments)
    level = models.CharField(max_length=100,choices=Levels)
    term = models.CharField(max_length=100,choices=Terms)
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = (( "student","department","level","term","year"),("student","term","year"))

    def __str__(self):
        return self.student.name+" to "+self.get_department_display()+" to "+self.get_level_display()+" to "+self.get_term_display()



############################################################################################################################


class StudentData(models.Model):
    # Relations
    student = models.OneToOneField(Students_user,on_delete=models.CASCADE,unique=True)
    # Variables
    studentData_code = models.PositiveIntegerField(unique=True)
    place = models.CharField(max_length=400)

# personal data
    studentPhoneNumber = models.CharField(max_length=15)
    identityNumber = models.CharField(max_length=25)
    nationality = models.CharField(max_length=100)
    age =models.PositiveIntegerField()
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    birthDate = models.DateField()
    image = models.ImageField(upload_to='profile', blank=True )

# communicaton data
    parentPhoneNumber = models.PositiveIntegerField()
    homeNumber = models.PositiveIntegerField()
    parentName = models.CharField(max_length=200)
    address =  models.CharField(max_length=200)

# Prequalfication 
    qualification = models.CharField(max_length=100)
    seatNumber = models.PositiveIntegerField()
    turn = models.CharField(max_length=100)
    grades = models.PositiveIntegerField()
    schoolYear = models.DateField()

# Post Secondary Education
    instituteName = models.CharField(max_length=100 , blank=True)
    instituteYear = models.DateField()

    def __str__(self):
        return self.student.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Upload, self).save(*args, **kwargs)
    def compressImage(self,image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image




############################################################################################################################

class Subject(models.Model):
    # Relations
    name = models.CharField(max_length=400,unique=True)
    dector = models.ManyToManyField(Doctors,related_name='subject112')
    TeachindAssistanc = models.ManyToManyField(TeachingAssistant,blank=True,related_name='subject113')
    lab_Assistanc=models.ManyToManyField(TeachingAssistant,blank=True,related_name='subject114')
    Requirement = models.ManyToManyField("self",blank=True,related_name='subject115')
    # Variables
    Specialization = models.CharField(max_length=100,choices=specialization)
    department = models.CharField(max_length=100,choices=Departments)
    no_hours = models.PositiveIntegerField()
    Optional = models.CharField(max_length=100,choices=optional)
    level = models.CharField(max_length=100,choices=Levels)
    term = models.CharField(max_length=100,choices=Terms)



    def __str__(self):
        return self.name




############################################################################################################################



class RegisterSubject(models.Model):
    # Relations
    subjects = models.ForeignKey(Subject,related_name='subject18',on_delete=models.SET_NULL,null=True)
    students = models.ForeignKey(Students,related_name='subject00',on_delete=models.CASCADE)
    current_D = models.ManyToManyField(Doctors,blank=True,related_name='subject19')
    current_A = models.ManyToManyField(TeachingAssistant,blank=True,related_name='subject110')
    current_L = models.ManyToManyField(TeachingAssistant,blank=True,related_name='subject111')
    # Variables
    department = models.CharField(max_length=100,choices=Departments,blank=True)
    level = models.CharField(max_length=100,choices=Levels,blank=True)
    term = models.CharField(max_length=100,choices=Terms,blank=True)
    year = models.PositiveIntegerField()
    sucses = models.BooleanField(blank=True)


    class Meta:
        unique_together = ( "students","subjects")



    def __str__(self):
        self.save()
        return self.students.student.name+" to "+self.subjects.name+" to "+str(self.year)









############################################################################################################################



# cho=(
# (1,Doctors.objects.get(pk=1).name),
# )



class Table(models.Model):
    # Relations
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    # Variables
    nameAction=models.CharField(max_length=100,choices=Action)
    interval=models.CharField(max_length=100,choices=interval)
    location=models.CharField(max_length=400)
    year=models.PositiveIntegerField()
    department = models.CharField(max_length=100,choices=Departments)
    term=models.CharField(max_length=100,choices=Terms)
    day=models.CharField(max_length=100,choices=day)
    doctor = models.ForeignKey(Doctors,blank=True,on_delete=models.SET_NULL,null=True)
    Assistant = models.ForeignKey(TeachingAssistant,blank=True,on_delete=models.SET_NULL,null=True)
    class Meta:
        unique_together = (("subject","day","interval","nameAction","location","year","term"),("day","interval","year","term","location"))

    def __str__(self):
        return self.subject.name+" "+self.nameAction




############################################################################################################################




class Degree(models.Model):
    # Relations
    subject=models.ForeignKey(RegisterSubject,related_name='subject12',on_delete=models.CASCADE)
    student=models.ForeignKey(Students,related_name='student31',on_delete=models.CASCADE)
    # Variables
    midterm=models.PositiveIntegerField(blank=True)
    final=models.PositiveIntegerField(blank=True ,default=50)
    total=models.PositiveIntegerField(blank=True)

    class Meta:
        unique_together = ("subject","student")

    def __str__(self):
        return self.subject.subjects.name+" to "+self.student.student.name





###################################################################################################################


class DEG(models.Model):
    name=models.CharField(max_length=100)#,choices=NameDeg)
    deg=models.PositiveIntegerField(blank=True)
    full=models.PositiveIntegerField(blank=True)
    show = models.BooleanField(blank=True)
    def __str__(self):
        return self.name


############################################################################################################################
class Absence(models.Model):
    name=models.PositiveIntegerField(blank=True)
    check=models.BooleanField(blank=True)
    def __str__(self):
        return str(self.name)
######################################################################################################################

class LectureDegree (models.Model):
    # Relations
    degr=models.ManyToManyField(DEG,blank=True)
    absence=models.ManyToManyField(Absence,blank=True)
    absence_degree=models.PositiveIntegerField(blank=True)
    absence_total=models.PositiveIntegerField(blank=True)
    lecture=models.OneToOneField(Degree,on_delete=models.CASCADE)
    lab=models.PositiveIntegerField(blank=True)
    # Variables
    total=models.PositiveIntegerField(blank=True)
    finsh = models.BooleanField(blank=True)
    def __str__(self):
        return self.lecture.subject.subjects.name+" to "+self.lecture.student.student.name



############################################################################################################################



class SectionDegree(models.Model):
    # Relations
    degr=models.ManyToManyField(DEG,blank=True)
    absence=models.ManyToManyField(Absence,blank=True)
    absence_degree=models.PositiveIntegerField(blank=True)
    absence_total=models.PositiveIntegerField(blank=True)
    section=models.OneToOneField(Degree,on_delete=models.CASCADE)
    # Variables
    full_degree=models.PositiveIntegerField(blank=True)
    total=models.PositiveIntegerField(blank=True)
    finsh = models.BooleanField(blank=True)
    def __str__(self):
        return self.section.subject.subjects.name+" to "+self.section.student.student.name




############################################################################################################################



class LABDegree(models.Model):
    # Relations
    absence=models.ManyToManyField(Absence,blank=True)
    absence_degree=models.PositiveIntegerField(blank=True)
    absence_total=models.PositiveIntegerField(blank=True)
    def __str__(self):
        return self.LAB.subject.subjects.name+" to "+self.LAB.student.student.name
