
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from index.models import BlogPost, SliderPhoto
from catalogue.models import Collection, Product, Shop

def index(request: HttpRequest):
    posts = BlogPost.objects.all()[0:5]
    slides = SliderPhoto.objects.all().order_by('precedence')
    product = Product.objects.first()
    collections = Collection.objects.filter(index_view=True)
    print(collections)
    return render(request, 'index.html', {
        'slides': slides,
        'posts': posts,
        'product': product,
        'collections': collections
    })

def about_us(request: HttpRequest):
    return render(request, 'aboutus.html')

def contact_us(request: HttpRequest):
    return render(request, 'contactus.html')

def cert(request: HttpRequest):
    return render(request, 'certs.html')

def add_p(request: HttpRequest):
    if request.method == 'POST':
        print(request.POST.get('a',None))
        print(request.POST.getlist('a', None))

        return HttpResponse('fff')
    return render(request, 'shop/add_product.html')


def shop(request: HttpRequest):
    shop = Shop.objects.first()
    return render(request, 'shop/shop.html', {
        'shop': shop
    })
    
def collection(request: HttpRequest):
    collection = Collection.objects.first()

    return render(request, 'shop/collection.html', {
        'collection': collection
    })

urlpatterns = [
    path('', index, name='index'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('aboutus/', about_us, name='aboutus' ),
    path('contactus/', contact_us, name='contactus' ),
    path('cert/', cert, name='cert' ),
    path('collection/', collection, name='col' ),
    path('shop/', shop, name='shop' ),
    path('add/', add_p, name='add' ),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users'), ),
    path('catalogue/', include('catalogue.urls', namespace='catalogue')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
