from django.shortcuts import  render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .admin import *

# Create your views here.
@login_required
def home(request):
    return render(request,"admin.html",{"col":4,"width":12})