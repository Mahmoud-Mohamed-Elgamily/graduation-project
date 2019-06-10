from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .admin import *

# Create your views here.
@login_required
def home(request):
    return render(request,"admin.html",{"col":4,"width":12})

@login_required
def student(request):
    return render(request,"bad/student.html",{"col":4,"width":12})

@login_required
def departmenet(request):
    return render(request,"bad/departmenet.html",{"col":12,"width":12})


@login_required
def controll(request):
    return render(request,"bad/controll.html",{"col":12,"width":12})

@login_required
def money(request):
    return render(request,"bad/money.html",{"col":12,"width":12})


@login_required
def register(request):
    return render(request,"bad/register.html",{"col":4,"width":12})


@login_required
def table(request):
    return render(request,"bad/table.html",{"col":12,"width":12})
