from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def stud(request):
    user = request.user
    if user.is_authenticated and user.is_teacher:
        return redirect('doctor:home')
    elif user.is_authenticated and user.is_student:
        return redirect('student:home')
    elif user.is_authenticated and user.is_assistant:
        return redirect('assistant:home')
    else:
        return render(request,'login.html')