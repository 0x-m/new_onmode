
from logging import LogRecord
from math import prod
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from httpx import delete

from .models import Collection, Comment, CreateShopRequest, Favourite, Option, Photo, Product, ProductFilter, ProductOptionValue, Shop
from .forms import CommentForm, CreateShopForm, ProductForm, ShopForm

# TODO: move to the shop custom manager!




@login_required
def product(request: HttpRequest, pid=None):
    '''
    Add or edit a product
    add a new product if pid is not specified 
    edit the product with id=pid if it is exist otherwise return 404 
    '''


    # Does user have any active shop ?
    user = request.user
    shop = get_object_or_404(Shop, owner=user, active=True)
    product = None
    if pid: #product exists if not return 404 
        product = get_object_or_404(Product, pk=pid, deleted=False)
    else:
        #request to add a new product
        if not shop.has_capacity():
            return HttpResponseNotAllowed() #TODO
        
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if not form.is_valid():
            return render(request, 'shop/add_product.html/', {
                'status':  form.errors,
                'product': product
            })

        # NOTE: any better way?
        if not product:
            # create a new product
            product = form.save(commit=False)
            product.shop = shop
            product.save()
        else:
            form.save() #update the product

        return render(request, 'shop/add_product.html/', {
            'status': 'edited' if prod else 'created',
            'product': product
        })

    return render(request, 'shop/add_product.html', {
        'product': product
    })


@login_required
def delete_product(request: HttpRequest, pid):
    ''' 
    Mark a product as deleted if the product with id=pid
    exists otherwise return http 404
    '''
    # Does the user have any active shop ?
    user = request.user
    shop = get_object_or_404(Shop, owner=user, active=True)
    product = get_object_or_404(Product,pk=pid, shop=shop, deleted=False)
    product.deleted = True
    product.save()
    return render(request, '')  # TODO



def filter(requeset: HttpRequest):
    form = ProductFilter(data=requeset.GET, 
                         queryset=Product.objects.filter(deleted=False).all(),
                         request=requeset)

    return render(requeset, 'shop/filter.html', {
        'filter': form
    })


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
        optval, created = ProductOptionValue.objects.get_or_create(
            product=product, option=option)
        if option.type in [Option.TYPES.Choices, Option.TYPES.MultiChoices]:
            option_value = ','.join(data.getlist('value')) + ',' #needed for filtering

        print(option_value, created)
        optval.value = option_value
        optval.save()
        return redirect('users:add-option', pid=pid)
    
        # return render(request, 'shop/product_options.html', {
        #     'product': product,
        #     'add_status': 'added' if created else 'edited',
        #     'option_name': option_name
        # })
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
            return redirect('users:add-option', pid=pid)
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
                return redirect('users:add-option', pid=pid)
            
            else:
                return HttpResponseBadRequest('Run out of storage.') ##make decent error page

        if url:
            product_photo = Photo(product=product, url=url)
            product.photo.save()
            return redirect('users:add-option', pid=pid)

    #...
    return HttpResponseNotAllowed(['POST'])


@login_required
def change_preview_photo(request: HttpRequest, pid):
    if request.method == 'POST':
        user = request.user
        shop = get_object_or_404(Shop, owner=user, active=True)
        product = get_object_or_404(Product,shop=shop, pk=pid, deleted=False)

        photo_id = request.POST.get('photo_id')
        if not photo_id:
            return HttpResponseBadRequest('photo_id is not provided')
        
        the_photo = product.photos.get(pk=photo_id)
        if the_photo:
            product.preview = the_photo
            product.save()
            return redirect('users:add-option', pid=pid)

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
            user.free_storage(the_photo.img.size) #TODO: move to the photo post delete!
            the_photo.img.delete() ##
            the_photo.delete()
            return redirect('users:add-option',pid=pid)
        except Photo.DoesNotExist:
            return HttpResponseNotFound('photo with  give id is not found')
    
    return HttpResponseNotAllowed(['POST'])




@login_required
def edit_shop(requeset: HttpRequest):

    # Does the user have any active shop if not return http404
    user = requeset.user
    shop = get_object_or_404(Shop, owner=user, active=True)

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


def collection(requeset: HttpRequest, collection_name):
    collection = get_object_or_404(Collection, en_name=collection_name)
    return render(requeset, 'shop/collection.html', {
        'collection': collection
    })
    

@login_required
def comment(request: HttpRequest):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            product = form.cleaned_data['product']
            
            comment, created = Comment.objects.update_or_create(user=user, 
                                                                product=product,
                                                                defaults=form.cleaned_data)
            if not created:
                comment.published = False
                
            form.save()
            return redirect(comment.product)
            
        else:
            return HttpResponseBadRequest()
       
    
    return HttpResponseNotAllowed(['POST'])
    

@login_required
def like(request: HttpRequest, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id, deleted=False)
    fav, created = Favourite.objects.get_or_create(user=user, product=product)
    if not created:
        fav.delete()
        
    return JsonResponse({
        'status': 'liked' if created else 'unliked'
    })

