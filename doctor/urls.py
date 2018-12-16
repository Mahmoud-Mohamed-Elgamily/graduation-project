"""UCMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app_name='doctor'
urlpatterns = [
    path('tbl/', views.tbl, name='tbl'),
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/<int:pk>/', views.students, name='students'),
    path('results/<int:pk>/', views.dgree, name='dgree'),
    path('addclm/<int:pk>/', views.AddClm, name='addclm'),
    path('absence/<int:pk>/', views.Absences, name='absence'),
    path('addabsence/<int:pk>/', views.addAbsences, name='addabsence'),
#
    path('stdata/', views.student_data, name='student_data'),
    path('results/', views.results, name='results'),
    path('absence/', views.absence, name='absence'),
    path('monitor/', views.monitor, name='monitor'),
    path('profile/', views.profile, name='profile'),
    path('mail/', views.mail, name='mail'),

]
