
from audioop import minmax
from mimetypes import common_types
from pickletools import read_uint1
from wsgiref.handlers import read_environ
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseServerError, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from httpx import RequestError

from promotions.models import GiftCard

#from catalog.models import Product

from .models import User, Wallet

from .forms import AddressForm, CheckoutForm, SignUpForm, VerificationCodeForm, ProfileForm
from .OTP import OTP, InvalidCodeException, ExpiredCodeException


def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_num = form.cleaned_data.get('phone_num', None)
            request.session['phone_num'] = phone_num
            request.session.save()

            OTP(request).clear()
            code = OTP(request).code
            # send verification code
            print(code)

            return redirect('users:verify')

        else:
            return render(request, 'user/signup.html', {
                'form': SignUpForm(),
                'error': form.errors
            })
    return render(request, 'user/signup.html', {
        'form': SignUpForm()
    })


def verify_code(request: HttpRequest):
    phone_num = request.session.get('phone_num', None)

    if not phone_num:
        return Http404()

    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)

        if not form.is_valid():
            return render(request, 'user/verify.html', {
                'error': 'invalid'
            })

        code = form.cleaned_data.get('code')
        try:
            otp = OTP(request)
            otp.check(code)
            user, _ = User.objects.get_or_create(phone_num=phone_num)
            # wallet,_ = Wallet.objects.get_or_create(user=user)

            login(request=request, user=user)
            del request.session['phone_num']
            request.session.save()
            return redirect('index')

        except InvalidCodeException:
            return render(request, 'user/verify.html', {
                'error': 'invalid code'
            })
        except ExpiredCodeException:
            del request.session['phone_num']
            request.session.save()
            return redirect('users:signup')
            # send again

    # get request
    return render(request, 'user/verify.html', {
        'form': VerificationCodeForm()
    })


# temp
def cart(request: HttpRequest):
    return render(request, 'shop/cart.html')


def notfound(request: HttpRequest):
    return render(request, '404.html')


def product(request: HttpRequest):
    return render(request, 'shop/product.html')


def store(request: HttpRequest):
    return render(request, 'shop/store.html')


def checkout_result(request: HttpRequest):
    return render(request, 'shop/checkout_result.html')


# def checkout(request: HttpRequest):
#     return render(request, 'shop/checkout.html')


@login_required
def profile(request: HttpRequest):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, 'user/dashboard/profile.html', {
                'status': 'invalid'
            })

        form.save()

        return render(request, 'user/dashboard/profile.html', {
            'status': 'edited successfully'
        })

    return render(request, 'user/dashboard/profile.html', {
        'form': ''
    })


@login_required
def addresses(request: HttpRequest):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if not form.is_valid():
            return render(request, 'user/dashboard/address.html', {
                'errors': form.errors
            })
        address = form.save(commit=False)
        address.user = request.user
        address.save()

        shop_name = request.POST.get('shop_name')
        if shop_name:
            return redirect('orders:checkout',shop_name=shop_name)
        
        return render(request, 'user/dashboard/address.html', {
            'errors': form.cleaned_data
        })

    return render(request, 'user/dashboard/address.html')


@login_required
def dashboard(request: HttpRequest):
    return render(request, 'user/dashboard/dashboard.html')


@login_required
def signout(request: HttpRequest):
    logout(request)
    return HttpResponse('loggedout')


@login_required
def wallet_checkout(request: HttpRequest):
    if request.method == 'POST':
        # TODO: move MIN_AMOUNT to .env
        MIN_AMOUNT = 100000
        MAX_AMOUNT = 10000000
        form = CheckoutForm(request.POST)

        if not form.is_valid():
            return render(request, 'user/dashboard/wallet.html', {
                'checkout_status': 'invalid_form'
            })

        status = None
        wallet = request.user.wallet
        amount = form.cleaned_data['amount']

        if not (MIN_AMOUNT <= amount <= MAX_AMOUNT):
            status = 'invalid_amount_range'

        if not wallet.has_balance(amount):
            status = 'wallet_has_no_enough_money'
            
        if status:
            return render(request, 'user/dashboard/wallet.html', {
                'checkout_status': status
            })

        c = form.save(commit=False)
        c.wallet = wallet
        c.save()

        return render(request, 'user/dashboard/wallet.html', {
            'checkout_status': 'success'
        })

    return Http404()


@login_required
def wallet_deposit(request: HttpRequest):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            return redirect('users:wallet')
        if amount.startswith('gift_'):
            try:
                gift = GiftCard.objects.get(code=amount)
                gift.apply(request.user)
                return redirect('users:wallet')
            except:
                return HttpResponse('not found....')
        
    return HttpResponseNotAllowed(['POST'])

# @login_required
# def set_password(request):
#     pass


# def comment(request: HttpRequest):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             product = data['product']
#             customer = request.user
#             data['customer'] = customer

#             _, created = Comment.objects.update_or_create(product=product, customer=customer,defaults=data)
#             response = 'comment updated successfully'
#             if created:
#                 response = 'comment added successfully'
#             return JsonResponse({'status': response})


#     # Handle get request.
#     return HttpResponseNotAllowed('POST')


@login_required
def comments(request: HttpRequest):
    # needs pagination
    # comments = request.user.comments.all()
    return render(request, 'user/dashboard/comments.html', {
        'comments': 'comments'
    })


def messages(request: HttpRequest):
    return render(request, 'user/dashboard/messages.html')


def orders(request: HttpRequest):
    return render(request, 'user/dashboard/orders.html')


def wallet(request: HttpRequest):
    return render(request, 'user/dashboard/wallet.html')


def about_shop(request: HttpRequest):
    return render(request, 'shop/about.html')


def shop_orders(request: HttpRequest):
    return render(request, 'shop/orders.html')


def shop_order(request: HttpRequest):
    return render(request, 'shop/order.html')

# @login_required
# def like(request: HttpRequest):
#     customer = request.user
#     fav, created = Favourite.objects.get_or_create(customer=customer)
#     if created:
#         fav.delete()

#     return JsonResponse({
#         'status': 'liked' if created else 'unliked'
#     })


@login_required
def favourites(request: HttpRequest):
    # likeds = request.user.favourites
    return render(request, 'user/dashboard/favourites.html', {
        'favourites': 'likeds'
    })


# def chekc_email(request: HttpRequest):
#     pass
