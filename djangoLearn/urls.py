
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from django.shortcuts import render



urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('base.urls'))
]
