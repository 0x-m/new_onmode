from asyncio import FastChildWatcher
from distutils.command.install_scripts import install_scripts
from doctest import FAIL_FAST
from itertools import product
from mimetypes import common_types
from pickletools import read_uint1
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import CreateShopRequest, Product, Shop
from .forms import CreateShopForm, ProductForm, ShopForm

# TODO: move to the shop custom manager!


def get_user_shop_or_404(user):
    ''' Get the user shop otherwise return 404 http error'''
    try:
        shop = Shop.objects.get(owner=user, is_active=True)
        return shop
    except Shop.DoesNotExist:
        return Http404()


@login_required
def product(request: HttpRequest, pid=None):
    '''
    Add or edit a product
    add a new product if pid is not specified 
    edit the product with id=pid if it is exist otherwise return 404 
    '''

    # Does user have any active shop ?
    shop = get_user_shop_or_404(request.user)

    # Does the (shop) have a product with id=pid ?
    prod = None
    if pid:
        try:
            prod = Product.objects.get(pk=pid, shop=shop, deleted=False)
        except Product.DoesNotExist:
            return Http404()
    else:
        # So user wants add a new product
        if not shop.has_capacity():
            pass  # TODO

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=prod)

        if not form.is_valid():
            return render(request, 'shop/add_product.html', {
                'status': 'invalid',
                'product': prod
            })

        # NOTE: any better way?
        if not prod:
            prod = form.save(commit=False)
            prod.shop = shop
            prod.save()
        else:
            form.save()

        return render(request, 'shop/add_product.html', {
            'status': 'edited' if prod else 'created',
            'product': prod
        })

    return render(request, 'shop/add_product.html', {
        'product': prod
    })


@login_required
def delete_product(request: HttpRequest, pid):
    ''' 
    Mark a product as deleted if the product with id=pid
    exists otherwise return http 404
    '''

    # Does the user have any active shop ?
    shop = get_user_shop_or_404(request.user)

    # Does the shop have a product with id=pid
    prod = None
    if pid:
        try:
            prod = Product.objects.filter(shop=shop, pk=pid, deleted=False)
        except Product.DoesNotExist:
            return Http404()

    prod.deleted = True
    prod.save()
    return render(request, '')  # TODO


def add_photo(requeset: HttpRequest):
    pass


def delete_photo(request: HttpRequest):
    pass


@login_required
def edit_shop(requeset: HttpRequest):

    # Does the user have any active shop if not return http404
    shop = get_user_shop_or_404(requeset.user)

    if requeset.method == 'POST':
        shop_form = ShopForm(requeset.POST, instance=shop)
        if not shop_form.is_valid():
            return render(requeset, 'shop/about.html', {
                'status': 'invalid'
            })

        shop_form.save()
        return render(requeset, 'shop/about.html', {
            'status': 'success',
            'shop': shop
        })

    return render(requeset, 'shop/about.html', {
        'shop': shop
    })


@login_required
def create_shop_request(request: HttpRequest):
    # Does the user have any shop...?
    # if so, it is not allowed to have more than one shop!
    if request.user.has_shop:
        return Http404()
    
    # Does the user have any request for creating a shop ?
    shop_req = None
    try:
        shop_req = CreateShopRequest.objects.get(user=request.user)
    except CreateShopRequest.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = None
        if shop_req:
            form = CreateShopForm(request.POST, instance=shop_req)
            # create shop request registered and not yet processed by admin
            # so it can not be edited.
            if not shop_req.rejected:
                return Http404()
            
            # admin rejected the request so, user must modify it.
            if form.is_valid():
                shop_req.rejected = False #so admin must revisit it.
                shop_req = form.save()
                return render(request, 'shop/create_shop.html', {
                    'status': 'edited',
                    'shop_req': shop_req
                })
            else:
                return render(request, 'shop/create_shop.html', {
                    'status': 'invalid name',
                    'shop_req': shop_req
                })
            
        else:
            # Create shop request does not exist so, create one...
            form = CreateShopForm(request.POST)
            if form.is_valid():
                shop_req = form.save(commit=False)
                shop_req.user = request.user
                shop_req.save()
                return render(request, 'shop/create_shop.html', {
                    'status': 'created',
                    'shop_req': shop_req
                })

    # Handle Get request.
    return render(request, 'shop/create_shop.html', {
        'status': '',
        'shop_req': shop_req
    })
                

  
