
from ssl import cert_time_to_seconds
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path, include



def index(request: HttpRequest):
    return render(request, 'index.html')

def about_us(request: HttpRequest):
    return render(request, 'aboutus.html')

def contact_us(request: HttpRequest):
    return render(request, 'contactus.html')

def cert(request: HttpRequest):
    return render(request, 'certs.html')


urlpatterns = [
    path('', index, name='index'),
    path('aboutus/', about_us, name='aboutus' ),
    path('contactus/', contact_us, name='contactus' ),
    path('cert/', cert, name='cert' ),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users'), )
]
