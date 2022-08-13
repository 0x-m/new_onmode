from django.urls import path

from . import views

app_name = 'index'

urlpatterns = [ 
    path('', views.index, name='index'),
    path('aboutus/', views.about_us, name='aboutus' ),
    path('contactus/', views.contact_us, name='contactus' ),
    path('certifications/', views.certificatinos, name='certifications' ),
    path('policies/', views.policies, name='policies' ),
    path('returnterms/', views.return_terms, name='return_terms' ),
    path('geo/cities/<province_id>', views.get_cities, name='get_cities'),
    path('pages/<slug>/', views.get_page, name='page')

]