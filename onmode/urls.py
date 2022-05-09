
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from index.models import About, BlogPost, Certificate, ShopSet, SliderPhoto, Law
from catalogue.models import Collection, Product, Shop

    
from catalogue.views import shop, search, category


def allp(request):
    return render(request, 'user/dashboard/create_ticket.html')

urlpatterns = [
    path('', include('index.urls', namespace='index')),
    path('', include('orders.urls', namespace='orders')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('allp/', allp),
    path('catalogue/', include('catalogue.urls', namespace='catalogue')),
    path('search/', search, name='search' ),
    path('users/', include('users.urls', namespace='users'), ),
    path('<shop_name>/', shop , name='shop'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
