from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def stud(request):
    return HttpResponse("ok")
