
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path, include



def index(request: HttpRequest):
    return render(request, 'index.html')

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users'), )
]
