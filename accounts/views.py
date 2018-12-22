from django.shortcuts import render,redirect
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
#from django.views.decorators.csrf import ensure_csrf_cookie
#from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from . import forms



# Create your views here.
def signup(request):
    #CSRF_COOKIE_SECURE=True
    
    if request.method=='POST':
        form=forms.UserCreateForm(request.POST)
        print(form)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('database:home')
        else:
            return render(request,"signup.html",{'form':form})
    else:
        form=forms.UserCreateForm()
    return render(request,"signup.html")

def user_login(request):
    print("request")
    print(request)
    logerro=False

    # handling logout
    if request.user.is_authenticated:
        logout(request)

    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_teacher:
                return redirect('doctor:home')
            elif user.is_authenticated and user.is_student:
                return redirect('student:home')
            else:
                print ("someone tried to login and failed!")
                print("username: {} and password: {}".format(username,password))
                logerro=True
                return render(request,'login.html',{'logerro':logerro})
    else:
        return render(request,'login.html',{'logerro':logerro})

def logout_view(request):
    logout(request)
    return redirect('database:home')


def home_page(request):
    return HttpResponse('<h1> welcome to the home! </h1>')