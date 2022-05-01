from asyncio import FastChildWatcher
import code
from curses import use_default_colors
from importlib.machinery import PathFinder
from importlib.metadata import PathDistribution
from itertools import product
import json
from math import prod
from mimetypes import common_types
from pickletools import read_uint1
from typing import get_origin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotModified, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from catalogue.models import Shop, Product
from users.models import Address
from promotions.models import Coupon

from .models import Order, OrderItem, ReturnRequest
from .forms import AcceptOrderForm, AddOrderItemForm


def cart(request: HttpRequest):
    orders = request.user.orders.filter(paid=False)
    return render(request, 'shop/cart.html', {
        'carts': orders
    })
    
@login_required
def refresh_order(request: HttpRequest):
    order_id = request.GET.get('id')
    order = get_object_or_404(Order, id=order_id, paid=False, user=request.user)
    order.refresh()
    # return redirect('orders:cart')
    return JsonResponse({
        'status': 'refereshed'
    })

  
def test(request: HttpRequest):

    if request.method == 'POST':
        form = AddOrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            
            return HttpResponse('correct')
        else:
            return HttpResponse(form.errors)
    
    return render(request,'shop/test.html', {
        'form': AddOrderItemForm()
    })
  
  
@login_required  
def add_item(request: HttpRequest):
    if request.method == 'POST':
        print(request.POST, 'post....')
        form = AddOrderItemForm(request.POST)
        if form.is_valid():
            user = request.user
            product = form.cleaned_data['product']
            shop = product.shop
            
            #TODO: users can not buy form theirselves
            order, _ = Order.objects.get_or_create(shop=shop, user=user, paid=False)

            #WARN: smelly code...!
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity = form.cleaned_data['quantity']
            order_item.options = form.cleaned_data['options']
            order_item.refresh() #ambiguous this method updates prices fields and save the model

            return JsonResponse({
                'status': 'added',
                'final_price': order.final_price,

            })
        else:
            print(form.errors,'////////////////')
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed(['POST'])
    


@login_required
def delete_item(request: HttpRequest, order_item_id):
    
    order_item = get_object_or_404(OrderItem, pk=order_item_id, order__user=request.user)
    
    order = order_item.order
    order_item.delete()
    if len(order) == 0:
        order.delete()
        
    return JsonResponse({
        'status': 'deleted',
        'final_price': order.final_price if order else 0,
        
    })

    
    

@login_required
def increment(request: HttpRequest, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id, order__user=request.user)
    try:
        order_item.increment()
    except:
        return HttpResponseBadRequest()

    return JsonResponse({
        'status': 'incremented',
        'final_price': order_item.order.final_price,
        'pp': order_item.product.compute_price(),
    })
    

@login_required
def decrement(request: HttpRequest, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id, order__user=request.user)
    order = order_item.order
    #TODO: need special exception
    try:
        order_item.decrement()
    except:
        order_item.delete()
    
    if len(order) == 0:
        order.delete()
        
    return JsonResponse({
        'status': 'decremented',
        'final_price': order.final_price if order else None
    })
    


@login_required
def checkout(request: HttpRequest, shop_name):
    shop = get_object_or_404(Shop,name=shop_name, active=True)
    user = request.user
    cart = get_object_or_404(Order,user=user, shop=shop, paid=False)
    ref_id = ''
    authority = ''
    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = Address.objects.get(pk=address_id, user=request.user)
        if not address:
            return render(request, 'shop/checkout.html', {
                'cart': cart,
                'status': 'invalid address'
            })
        cart.address = address
        cart.save()
        return redirect('https://www.google.com')
        # if not cart.paid:
        #     cart.pay(ref_id, authority)
        #     return render(request, 'shop/checkout_result.html', {
        #         'order': cart
        #     })
        
        
    return render(request, 'shop/checkout.html', {
        'cart': cart
    })


@login_required
def verify_payment(request: HttpRequest):
    pass

@login_required
def accept(request: HttpRequest):
    
    if not request.user.shop:
        return Http404()
    
    if request.method == 'POST':
        form = AcceptOrderForm(request.POST)
        if form.is_valid():
            shop = form['shop']
            order = form['order']
            if not request.user.shop == shop:
                return HttpResponseForbidden('you dont have permission to do this')
            order.accep()
                
            
    
    return HttpResponseNotAllowed(['POST'])


@login_required
def tarcking_code(request: HttpRequest):
    
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])


    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        id = request.POST.get('order_id')
        order = get_object_or_404(Order, paid=False, shop=request.user.shop, pk=id)
        order.tracking_code = tracking_code
        order.save()
        return redirect(order)



@login_required
def reject(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    if request.method == 'POST':
        id = request.POST.get('irder_id')
        msg = request.POST.get('reject_msg', '')
        order = get_list_or_404(Order, pk=id, shop=request.user.shop, paid=False)
        order.reject(msg)
        return redirect(order)


@login_required
def canceled(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        shop_id = request.POST.get('shop_Id')

        order = get_list_or_404(Order, pk=order_id, user=request.user, shop__pk=shop_id, paid=False)
        order.canceled()
        return redirect(order)
    
    
@login_required
def fulfill(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        shop_id = request.POST.get('shop_id')
        
        order = get_list_or_404(Order, pk=order_id, user=request.user, shop__pk=shop_id)
        order.fulfill()
        
        return redirect(order)
    

@login_required
def user_order(request: HttpRequest, order_code):
    order = get_object_or_404(Order, code=order_code, user=request.user)
    return redirect(order)

@login_required
def seller_order(request: HttpRequest, order_code):
    order = get_object_or_404(Order, code=order_code, shop=request.user.shop)
    return redirect(order)



@login_required
def set_coupon(request: HttpRequest):
    if request.method == 'POST':
      
        coupon_code = request.POST.get('code')
        order_id = request.POST.get('order_id')
        
        if not coupon_code or not order_id:
            return HttpResponseBadRequest()
        
        # coupon  = Coupon.objects.filter(code=coupon_code, used=False).first()
        coupon = get_object_or_404(Coupon, code=coupon_code, used=False)
        order = get_object_or_404(Order, pk=order_id, paid=False, user=request.user)
        # order = Order.objects.filter(pk=order_id, user=request.user, paid=False)

        if coupon.is_valid():
            order.set_coupon(coupon)
            return JsonResponse({
                'status': 'set',
                'final_price': order.final_price
            })
        else:
            return JsonResponse({
                'status': 'invalid',
                'final_price': order.fina_price
            })
                
    return HttpResponseNotAllowed(['POST'])
   

@login_required
def delete_coupon(request: HttpRequest):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        if not order_id:
            return HttpResponseBadRequest()
        
        order = get_object_or_404(Order, pk=order_id, user=request.user, paid=False)
        if order.coupon:
            order.delete_coupon()
            return JsonResponse({
                'status': 'deleted',
                'final_price': order.final_price
            })
        return JsonResponse({
            'status': 'coupon was not found'
        })
        
    return HttpResponseNotAllowed(['POST'])


        
        
            