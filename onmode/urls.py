
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from index.models import About, BlogPost, Certificate, ShopSet, SliderPhoto, Law
from catalogue.models import Collection, Product, Shop

def index(request: HttpRequest):
    posts = BlogPost.objects.all()[0:5]
    slides = SliderPhoto.objects.all().order_by('precedence')
    product = Product.objects.first()
    collections = Collection.objects.filter(index_view=True)
    print(collections)
    shopset = ShopSet.objects.first()
    
    return render(request, 'index.html', {
        'slides': slides,
        'posts': posts,
        'product': product,
        'collections': collections,
        'shopset': shopset,
    })

def about_us(request: HttpRequest):
    return render(request, 'aboutus.html', {
        'law': Law.objects.first()
    })

def contact_us(request: HttpRequest):
    return render(request, 'contactus.html')

def cert(request: HttpRequest):
    return render(request, 'certs.html')


    
from catalogue.views import shop, search, category

urlpatterns = [
    path('', include('index.urls', namespace='index')),
    path('', include('orders.urls', namespace='orders')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('aboutus/', about_us, name='aboutus' ),
    path('contactus/', contact_us, name='contactus' ),
    path('search/', search, name='search' ),
    path('category/<category_name>', category, name='category' ),
    path('cert/', cert, name='cert' ),
    path('<shop_name>/', shop , name='shop'),
    path('users/', include('users.urls', namespace='users'), ),
    path('catalogue/', include('catalogue.urls', namespace='catalogue')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
