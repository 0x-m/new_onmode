
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path, include



def index(request: HttpRequest):
    return render(request, 'index.html')

def about_us(request: HttpRequest):
    return render(request, 'aboutus.html')

def contact_us(request: HttpRequest):
    return render(request, 'index.html')

def rules(request: HttpRequest):
    return render(request, 'index.html')


urlpatterns = [
    path('', index, name='index'),
    path('/aboutus', about_us, name='aboutus' ),
    path('/contactus', contact_us, name='contactus' ),
    path('/rules', rules, name='rules' ),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users'), )
]
