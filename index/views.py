from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render

from .forms import ContactUsForm
from .models import *
from catalogue.models import Product, Collection


def about_us(request: HttpRequest):
    return render(request, 'aboutus.html', {
        'about': About.objects.first()
    })


def policies(request: HttpRequest):
    return render(request, 'laws.html', {
        'law': Law.objects.first()
    })

def certificatinos(request: HttpRequest):
    return render(request, 'certs.html', {
        
    })

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

def contact_us(request: HttpRequest):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contactus.html', {
                'status': 'success'
            })
        return render(request, 'contactus.html', {
            'status': 'faild'
        })

    
    return render(request, 'contactus.html')


