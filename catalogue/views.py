
from math import prod
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from httpx import delete

from .models import CreateShopRequest, Option, Photo, Product, ProductOptionValue, Shop
from .forms import CreateShopForm, ProductForm, ShopForm

# TODO: move to the shop custom manager!


def get_user_shop_or_404(user):
    ''' Get the user shop otherwise return 404 http error'''
    try:
        shop = Shop.objects.get(owner=user, active=True, deleted=False)
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
        # colors = request.POST.getlist('colors', None)
        # sizes = request.POST.getlist('sizes', None)
        # categories = request.POST.getlist('categories', None)
        # brand = request.POST.get('brand', None)
        print(request.POST['attributes'])
        if not form.is_valid():
            return render(request, 'shop/add_product.html/', {
                'status':  form.errors,
                'product': prod
            })

        # NOTE: any better way?
        if not prod:
            prod = form.save(commit=False)
            prod.shop = shop
            prod.save()
        else:
            form.save()

        return render(request, 'shop/add_product.html/', {
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





@login_required
def add_option(request: HttpRequest, pid):
    if not request.user.has_shop:
        return Http404()

    product = get_object_or_404(
        Product, shop=request.user.shops.first(), pk=pid, deleted=False)

    if request.method == 'POST':
        data = request.POST
        option_name = data.get('name', None)
        option_value = data.get('value', None)
        if not (option_name and option_value):
            return HttpResponseBadRequest('empty fields')

        option = get_object_or_404(Option, name=option_name)
        _, created = ProductOptionValue.objects.update_or_create(
            product=product, option=option)
        if option.type in [Option.TYPES.Choices, Option.TYPES.MultiChoices]:
            option_value = data.getlist('value')

        option.value = option_value
        option.save()
        return render(request, 'shop/product_options.html', {
            'product': product,
            'add_status': 'added' if created else 'edited',
            'option_name': option_name
        })
    return render(request, 'shop/product_options.html', {
        'product': product
    })


@login_required
def delete_option(request: HttpRequest, pid):
    if not request.user.has_shop:
        return Http404()

    product = get_object_or_404(
        Product, pk=pid, shop=request.user.shops.first(), deleted=False)

    if request.method == 'POST':
        option_name = request.POST.get('name', None)
        if not option_name:
            return HttpResponseBadRequest()

        option = product.options.all().filter(name=option_name).first()
        if option:
            option.delete()
            return render(request, 'shop/product_options.html', {
                'option_name': option_name,
                'delete_status': 'deleted',
                'product': product
            })
        else:
            return Http404()

    return HttpResponseNotAllowed(['POST'])


@login_required
def add_photo(request: HttpRequest, pid):

    if request.method == 'POST':
        user = request.user
        shop = get_object_or_404(Shop, owner=user, active=True)
        product = get_object_or_404(Product, pk=pid, shop=shop, deleted=False)

        photo = request.FILES.get('photo', None)
        url = request.POST.get('url')
        alt_text = request.POST.get('alt')
        
        if not (photo or url):
            return HttpResponseBadRequest('empty fields' + 'url:' + str(url) + 'img:' + str(photo))

        # in MBytes
        if photo:
            photo_size = photo.size  # in bytes
            if user.storage_has_capacity(photo_size):
                product_photo = Photo(product=product, img=photo, alt=alt_text)
                product_photo.save()
                user.consume_storage(photo_size)  # IMPORTANT....

                return render(request, 'shop/product_options.html', {
                    'phto_status': 'added',
                    'product': product
                })
            else:
                return HttpResponseBadRequest('Run out of storage.')

        if url:
            product_photo = Photo(product=product, url=url)
            product.photo.save()
            return render(request, 'shop/product_options.html', {
                'phto_status': 'added',
                'product': product
            })

    #...
    return HttpResponseNotAllowed(['POST'])


@login_required
def change_preview_photo(request: HttpRequest, pid):
    if request.method == 'POST':
        user = request.user
        shop = get_object_or_404(Shop, onwer=user, active=True)
        product = get_object_or_404(Product,shop=shop, pk=pid, deleted=False)

        photo_id = request.POST.get('photo_id')
        if not photo_id:
            return HttpResponseBadRequest('photo_id is not provided')
        
        the_photo = product.photos.get(pk=photo_id)
        if the_photo:
            product.preview = the_photo
            return render(request, 'sop/prodcut_options.html', {
                'change_preview_status': 'success',
                'product': product
            })

    return HttpResponseNotAllowed(['POST'])

@login_required
def delete_photo(request: HttpRequest, pid):
    if request.method == 'POST':
        user = request.user
        shop = get_object_or_404(Shop,owner=user, active=True)
        product = get_object_or_404(Product, pk=pid, shop=shop, deleted=False)
        photo_id = request.POST.get('photo_id')
        if not photo_id:
            return HttpResponseBadRequest('photo id is not entered')
        try:
            the_photo = product.photos.get(pk=photo_id)
            the_photo.img.delete()
            return render(request, 'shop/product_options.html', {
                'delete_photo_status': 'deleted',
                'product': product
            })
        except Photo.DoesNotExist:
            return HttpResponseNotFound('photo with  give id is not found')
    
    return HttpResponseNotAllowed(['POST'])




@login_required
def edit_shop(requeset: HttpRequest):

    # Does the user have any active shop if not return http404
    shop = get_user_shop_or_404(requeset.user)

    if requeset.method == 'POST':
        shop_form = ShopForm(requeset.POST, instance=shop)
        if not shop_form.is_valid():
            return render(requeset, 'shop/about.html', {
                'status': 'invalid',
                'shop': shop
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
                shop_req.rejected = False  # so admin must revisit it.
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
