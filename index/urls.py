from numbers import Real
from django.urls import path

from . import views

app_name = 'index'

urlpatterns = [ 
    path('', views.index, name='index'),
    path('aboutus/', views.about_us, name='aboutus' ),
    path('contactus/', views.contact_us, name='contactus' ),
    path('certifications/', views.certificatinos, name='certifications' ),
    path('policies/', views.policies, name='policies' ),
]