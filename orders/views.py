from importlib.machinery import PathFinder
from mimetypes import common_types
from typing import get_origin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotModified, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from catalogue.models import Shop, Product

from .models import Order, OrderItem, ReturnRequest
from .forms import AcceptOrderForm, AddOrderItemForm


def cart(request: HttpRequest):
    orders = request.user.orders.filter(paid=False)
    return render(request, 'shop/cart.html', {
        'carts': orders
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
        form = AddOrderItemForm(request.POST)
        if form.is_valid():
            shop = form.product.shop
            
            #TODO: users can not buy form theirselves
            order = Order.objects.get_or_create(shop=shop, user=request.user, paid=False)

            order_item = OrderItem.objects.get_or_create(order=order, product=form.product)
            form.instance = order_item
            form.instance.update() #ambiguous 
           # form.save()
           # order_item.refresh() #ambiguous!!
            return JsonResponse({
                'status': 'added'
            })
    
    
@login_required
def delete_item(request: HttpRequest):
    pass

@login_required
def increment(request: HttpRequest, order_id):
    pass

def decrement(request: HttpRequest):
    pass


def checkout(request: HttpRequest, shop_name):
    shop = get_object_or_404(Shop,name=shop_name, active=True)
    user = request.user
    cart = Order.objects.get(user=user, shop=shop, paid=False)
    ref_id = ''
    authority = ''
    if request.method == 'POST':
        #check for payment:
        # pay cart if payment is valid:
        if not cart.paid:
            cart.pay(ref_id, authority)
            return render(request, 'shop/checkout_result.html', {
                'order': cart
            })
        
        
    return render(request, 'shop/checkout.html', {
        'cart': cart
    })


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

