
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from index.models import BlogPost, ShopSet, SliderPhoto
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
        'shopset': shopset
    })

def about_us(request: HttpRequest):
    return render(request, 'aboutus.html')

def contact_us(request: HttpRequest):
    return render(request, 'contactus.html')

def cert(request: HttpRequest):
    return render(request, 'certs.html')

def shop(request: HttpRequest):
    shop = Shop.objects.first()
    return render(request, 'shop/shop.html', {
        'shop': shop
    })
    
from catalogue.views import shop, search, category

urlpatterns = [
    path('', index, name='index'),
    path('', include('orders.urls', namespace='orders')),
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
