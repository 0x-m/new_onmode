
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem

from catalogue.models import Product, Shop



def cart(request: HttpRequest):
    url = request.POST.get('back_url')
    print(url)
    return render(request, 'shop/cart.html', {
        'back_url': url
    })
    

def checkout(request: HttpRequest, shop_name):
    shop = get_object_or_404(Shop,name=shop_name, active=True)
    user = request.user
    cart = Cart.objects.get(user=user, shop=shop)
    return render(request, 'shop/checkout.html', {
        'cart': cart
    })


def add_item(request: HttpRequest, pid):
    user = request.user
    product = get_object_or_404(Product, pk=pid, deleted=False)
    quantity = request.POST.get('quantity')
    options = request.POST.get('options')
    #TODO: check options validity
    
    if not quantity:
        quantity = 1
    # a shopkeeper cant buy his product
    shop = product.shop

    #TODO: user can not but form his(her)self
    # if user.shop == shop:
    #     # TODO: design error page
    #     return HttpResponseForbidden('you can not buy from yourself')

    cart, _ = Cart.objects.get_or_create(user=user, shop=shop)
    item , created =  CartItem.objects.get_or_create(product=product, cart=cart)
    item.price = product.compute_price() #TODO: use signals
    
    if quantity:
        item.quantity = quantity
    if options:
        item.options = options

    item.save()
    
    return JsonResponse({"result": "added" if created else "edited"})


def delete_item(request: HttpRequest, pid):
    user = request.user
    product = get_object_or_404(Product, pk=pid, deleted=False)
    item = get_object_or_404(CartItem, product=product, cart__user=user)
    cart = item.cart
    item.delete()
    if len(cart) == 0:
        cart.delete()
    return redirect('cart:cart')


def increment_item(request: HttpRequest, pid):
    user = request.user
    product = get_object_or_404(Product, pk=pid, deleted=False)
    item = get_object_or_404(CartItem, product=product, cart__user=user)
    item.increment()
    cart = item.cart
    return redirect('cart:cart')


def decrement_item(request: HttpRequest, pid):
    user = request.user
    product = get_object_or_404(Product, pk=pid, deleted=False)
    item = get_object_or_404(CartItem, product=product, cart__user=user)
    cart = item.cart
    try:
         item.decrement()
    except:
        item.delete()
        if len(cart) == 0:
            cart.delete()
    return redirect('cart:cart')

    # return JsonResponse({
    #     'total': cart.total,
    #     'quantity': len(cart),
    #     'final_price': cart.final_price
    # })
