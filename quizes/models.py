from django.db import models
import random
from django.contrib.auth.models import User
from database.models import Students_user
# Create your models here.

choose=(
("A","A"),
("B","B"),
("C","C"),
("D","D"),
)


class questions(models.Model):
    questions =models.CharField(max_length=500,unique=True)

    # Choose
    A = models.CharField(max_length=100)
    B = models.CharField(max_length=100)
    C = models.CharField(max_length=100)
    D = models.CharField(max_length=100)
    correct=models.CharField(max_length=100,choices=choose)


    # class Meta:
    #     unique_together = ( ("A","B"),("A","C"),("A","D"),("B","C"),("B","D"),("C","D"))

    def __str__(self):
        return self.questions


passRandom=["~","!","@","#","$","%","^","&","&","*","(",")","_","+","Q","W","E","R","T","Y","U","I","","O","P","{","}","A","S","D","F","G","H","J","K","L",":","|","?",">","<","M","N","B","V","C","X","Z","1","2","3","4","5","6","7","8","9","0",".","q","w","e","r","t","y","u","i","o","p","[","]",";","l","k","j","h","g","f","d","s","a","z","x","c","v","b","n","m",",",".","/","-","="]



class students(models.Model):
    questions = models.ManyToManyField(questions,related_name='AS',blank=True)
    no_of_enter = models.PositiveIntegerField(blank=True)
    last_time = models.CharField(max_length=50,blank=True)
    time=models.CharField(max_length=50,blank=True)
    user = models.OneToOneField(Students_user,related_name='DF474',on_delete=models.CASCADE,blank=True)
    ip=models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=500,unique=True,blank=True)
    code = models.PositiveIntegerField(blank=True)
    password = models.CharField(max_length=10,blank=True)
    Degree = models.PositiveIntegerField(blank=True)
    finsh = models.BooleanField(blank=True)

    def save(self, *args, **kwargs):
        self.name=self.user.name
        super(students, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
