
from tkinter.messagebox import NO
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotModified, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from catalogue.models import Shop, Product
from users.models import Address
from promotions.models import Coupon
import requests
from .models import Order, OrderItem
from .forms import AcceptOrderForm, AddOrderItemForm
from django.core.paginator import *
from decouple import config
from index.models import GeoLocation




def cart(request: HttpRequest):
    orders = []
    if request.user.is_authenticated:
        orders = request.user.orders.filter(paid=False)
    return render(request, 'shop/cart.html', {
        'carts': orders
    })



@login_required
def refresh_order(request: HttpRequest, order_id):
    order = get_object_or_404(
        Order, id=order_id, paid=False, user=request.user)
    order.refresh()
    return redirect('orders:cart')
    # return JsonResponse({
    #     'status': 'refereshed'
    # })




@login_required
def add_item(request: HttpRequest):
    if request.method == 'POST':
        print(request.POST, 'post....')
        form = AddOrderItemForm(request.POST)
        if form.is_valid():
            user = request.user
            product = form.cleaned_data['product']
            shop = product.shop

            # users can not buy form theirselves
            if user.shop == shop:
                print('invalid')
                return JsonResponse({
                    'status': 'invalid action'
                })
                
            order, _ = Order.objects.get_or_create(
                shop=shop, user=user, paid=False)

            # WARN: smelly code...!
            order_item, created = OrderItem.objects.get_or_create(
                order=order, product=product)
            order_item.quantity = form.cleaned_data['quantity']
            order_item.options = form.cleaned_data['options']
            order_item.refresh()  # ambiguous this method updates prices fields and save the model
            print(order_item.final_price)
            print('added....')
            return JsonResponse({
                'status': 'added',
                'final_price': order.final_price,
                'cart': request.user.cart_count


            })
        else:
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed(['POST'])


@login_required
def delete_item(request: HttpRequest, order_item_id):
    print('delete issued')
    order_item = get_object_or_404(
        OrderItem, pk=order_item_id, order__user=request.user)

    order = order_item.order
    order_item.delete()
    if len(order) == 0:
        order.delete()

    return JsonResponse({
        'status': 'deleted',
        'final_price': order.final_price if order else 0,
        'cart': request.user.cart_count


    })


@login_required
def increment(request: HttpRequest, order_item_id):
    order_item = get_object_or_404(
        OrderItem, pk=order_item_id, order__user=request.user)
    try:
        order_item.increment()
    except:
        return HttpResponseBadRequest()

    return JsonResponse({
        'status': 'incremented',
        'final_price': order_item.order.final_price,
        'pp': order_item.product.compute_price(),
        'cart': request.user.cart_count
    })


@login_required
def decrement(request: HttpRequest, order_item_id):
    order_item = get_object_or_404(
        OrderItem, pk=order_item_id, order__user=request.user)
    order = order_item.order
    # TODO: need special exception
    try:
        order_item.decrement()
    except:
        order_item.delete()

    if len(order) == 0:
        order.delete()

    return JsonResponse({
        'status': 'decremented',
        'final_price': order.final_price if order else None,
        'cart': request.user.cart_count

    })


@login_required
def checkout(request: HttpRequest, shop_name):
    shop = get_object_or_404(Shop, name=shop_name, active=True)
    user = request.user
    cart = get_object_or_404(Order, user=user, shop=shop, paid=False)
    wallet_has_balance = request.user.wallet.has_balance(cart.final_price)

    provinces = GeoLocation.objects.first()
    if provinces:
        provinces = provinces.provinces
        
    if request.method == 'POST':
        address_id = request.POST.get('address')
        order_msg = request.POST.get('order_msg')
        pay_via = request.POST.get('pay_via')
        address = None
        try:
            address = Address.objects.get(pk=address_id, user=request.user)
        except Address.DoesNotExist:
            return render(request, 'shop/checkout.html', {
                'cart': cart,
                'address_status': 'invalid address' if not address else '',
                'pay_status': 'invalid pay_via' if not pay_via else '',
                'wallet_has_balance': wallet_has_balance,
                'provinces': provinces if provinces else None
            })

        cart.address = address
        cart.order_msg = order_msg

        if pay_via == 'wallet':
            cart.pay_via = Order.PAYSOURCE.WALLET
        elif pay_via == 'direct':
            cart.pay_source = Order.PAYSOURCE.DIRECT

        cart.save()

        if pay_via == 'direct':
            merchant_id = config('MERCHANT_ID', '')
            params = {
                'merchant_id': merchant_id,
                'amount': cart.final_price,
                'callback_url': 'https://localhost:800/orders/verify',
                'currency': 'IRT',
                'description': cart.description,
                'metadata': {
                    'mobile': request.user.phone_num
                }
            }
            headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
            }

            req_result = requests.post('https://api.zarinpal.com/pg/v4/payment/request.json',
                                       headers=headers, json=params)
            res = req_result.json()
            if res['data']['code'] == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + res['data']['authority'])
            else:
                return render(request, 'shop/checkout.html', {
                    'cart': cart,
                    'address_status': 'invalid address' if not address else '',
                    'pay_status': 'invalid pay_via' if not pay_via else '',
                    'wallet_has_balance': wallet_has_balance,
                    'connection': 'error',
                    'provinces': provinces if provinces else None

                })

        elif pay_via == 'wallet':
            if wallet_has_balance:
                cart.pay('site wallet', cart.code)
                return render(request,'shop/checkout_result.html', {
                    'ref_id': cart.code,
                    'status': 'success'
                })
            else:
                return Http404()

       
        # if not cart.paid:
        #     cart.pay(ref_id, authority)
        #     return render(request, 'shop/checkout_result.html', {
        #         'order': cart
        #     })

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'wallet_has_balance': wallet_has_balance,
        'provinces': provinces if provinces else None


    })


@login_required
def verify_payment(request: HttpRequest, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if request.GET.get('Status') == 'OK':
        authority = request.GET.get('Authority')
        merchant_id = config('MERCHANT_ID', '')
        params = {
            'merchant_id': merchant_id,
            'authority': authority,
            'amount': order.final_price,
        }

        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        req = requests.post('', headers=headers, params=params)

        res = None
        try:
            res = req.json()
        except:
            return Http404()

        if res['data']['code'] == 100:
            ref_id = res['data']['ref_id']
            order.pay(ref_id, authority)
            return render(request, 'shop/checkout_resut', {
                'ref_id': ref_id,
                'status': 'success',
                'pay_via': 'direct'
            })
        elif res['code'] == 101:
            return render(request, 'shop/checkout_result.html', {
                'status': 'success',
                'ref_id': ref_id,
                'pay_via': 'direct'
            })
        else:
            return render(request, 'shop/checkout_result.html', {
                'status': 'faild',
                'status_code': str(res['data']['code'])
            })
    else:
        return render(request, 'shop/checkout_result.html', {
            'status': 'faild'
        })


@login_required
def accept(request: HttpRequest):
    #seller must accept...
    
    if not request.user.shop:
        return Http404()

    if request.method == 'POST':
        shop = request.user.shop
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, shop=shop, pk=order_id, paid=False)
        order.accept()
        return redirect('orders:shop_order', order_code=order.code)
    
    return HttpResponseNotAllowed(['POST'])


@login_required
def tracking_code(request: HttpRequest):

    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        order_id = request.POST.get('order_id')
        order = get_object_or_404(
            Order, paid=False, shop=request.user.shop, pk=order_id)

        order.set_tracking_code(tracking_code)
        return redirect('orders:shop_order', order_code = order.code)



@login_required
def reject(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    if request.method == 'POST':
        order_id = request.POST.get('irder_id')
        msg = request.POST.get('reject_msg', '')
        order = get_list_or_404(
            Order, pk=order_id, shop=request.user.shop, paid=False)

        order.reject(msg)
        return redirect('orders:shop_order', order_code=order.code)


@login_required
def cancel(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        shop_id = request.POST.get('shop_Id')
        cancel_msg = request.POST.get('cancel_msg', '')
        order = get_list_or_404(
            Order, pk=order_id, user=request.user, shop__pk=shop_id, paid=False)
        order.cancel()

        return redirect('orders:shop_order', order_code=order.code)


@login_required
def fulfill(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        shop_id = request.POST.get('shop_id')

        order = get_object_or_404(
            Order, pk=order_id, user=request.user, shop__pk=shop_id)
        order.fulfill()
        return redirect('orders:shop_order', order_code=order.code)


@login_required
def user_order(request: HttpRequest, order_code):
    order = get_object_or_404(Order, code=order_code, user=request.user)
    return render(request, 'user/dashboard/order.html', {
        'order': order
    })


@login_required
def user_orders(request: HttpRequest):
    state = request.GET.get('state', 'pending')
    paginator = Paginator(request.user.orders.filter(state=state).all(), 20)
    pg = request.GET.get('page')
    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, 'user/dashboard/orders.html', {
        'page': page,
        'state': state
    })

@login_required
def shop_order(request: HttpRequest, order_code):
    order = get_object_or_404(Order, code=order_code, shop=request.user.shop)
    return render(request, 'shop/order.html', {
        'order':order
    })
    
@login_required
def shop_orders(request: HttpRequest):
    state = request.GET.get('state', 'pending')

    paginator = Paginator(request.user.shop.orders.filter(state=state).all(), 20)
    pg = request.GET.get('page')
    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    
    return render(request, 'shop/orders.html', {
        'page': page,
        'state': state
    })





@login_required
def set_coupon(request: HttpRequest):
    if request.method == 'POST':

        coupon_code = request.POST.get('code')
        order_id = request.POST.get('order_id')

        if not coupon_code or not order_id:
            return HttpResponseBadRequest()

        # coupon  = Coupon.objects.filter(code=coupon_code, used=False).first()
        coupon = get_object_or_404(Coupon, code=coupon_code, used=False)
        order = get_object_or_404(
            Order, pk=order_id, paid=False, user=request.user)
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

        order = get_object_or_404(
            Order, pk=order_id, user=request.user, paid=False)
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
