

'''

author: hamze ghaedi (github: 0x-m)

'''


from ast import expr_context
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseServerError, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from httpx import RequestError
from ippanel import Client
from decouple import config
import requests
from index.models import GeoLocation

from promotions.models import GiftCard

# from catalog.models import Product

from .models import DepositTransaction, Message, Ticket, TicketType, User, Wallet

from .forms import AddressForm, CheckoutForm, EmailCheckerForm, SignUpForm, TicketForm, TicketReplyForm, VerificationCodeForm, ProfileForm
from .OTP import OTP, InvalidCodeException, ExpiredCodeException




#helper functions--------------------
def send_verification_code(phone, code):
    api_key = config('VERIFICATION_SMS_API_KEY')
    sms = Client(api_key)
    pattern_values ={
    "verification_code": code
    }
    pattern_code = config('VERIFICATION_CODE_SMS_CODE')
    num = config('SMS_NUMBER')
    is_sent = sms.send_pattern(pattern_code,num, phone, pattern_values)
    return is_sent
#------------------------------------
    


def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_num = form.cleaned_data.get('phone_num', None)
            
            user = User.objects.filter(phone_num=phone_num).first()
            if user:
                if not user.is_active:
                    return render(request, 'limited_access.html')
            
            request.session['phone_num'] = phone_num
            request.session.save()

            OTP(request).clear()
            code = OTP(request).code
            res = send_verification_code(phone_num, code)
            # print(code)
            # res = True
            if res:
                return redirect('users:verify')
            else:
                return HttpResponseBadRequest() #TODO: make a decent error page

        else:
            return render(request, 'user/signup.html', {
                'form': SignUpForm(),
                'errors': form.errors
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

            login(request=request, user=user)
            del request.session['phone_num']
            request.session.save()
            return redirect('index:index')

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


@login_required
def profile(request: HttpRequest):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, 'user/dashboard/profile.html', {
                'status': 'invalid',
            })

        form.save()

        return render(request, 'user/dashboard/profile.html', {
            'status': 'edited successfully',

        })

    return render(request, 'user/dashboard/profile.html', {
        
    })


@login_required
def addresses(request: HttpRequest):
    geoloc = GeoLocation.objects.first()

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if not form.is_valid():
            return render(request, 'user/dashboard/address.html', {
                'errors': form.errors,
                'provinces': geoloc.provinces if geoloc else None
            })
        address = form.save(commit=False)
        address.user = request.user
        address.save()

        shop_name = request.POST.get('shop_name')
        if shop_name:
            return redirect('orders:checkout', shop_name=shop_name)

        return render(request, 'user/dashboard/address.html', {
            'errors': form.cleaned_data,
            'provinces': geoloc.provinces if geoloc else None
        })

    return render(request, 'user/dashboard/address.html', {
        'provinces': geoloc.provinces if geoloc else None
    })


@login_required
def dashboard(request: HttpRequest):
    return render(request, 'user/dashboard/dashboard.html')


@login_required
def signout(request: HttpRequest):
    logout(request)
    return redirect('index:index')


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
        try:
            amount = int(amount)
        except:
            amount = 0
            
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
        else:
            merchant_id = config('MERCHANT_ID', '')
            params = {
                'merchant_id': merchant_id,
                'amount': amount,
                'callback_url': reverse('users:deposit-verify', kwargs= {'amount': amount}) ,
                'currency': 'IRT',
                'description': 'wallet deposit',
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
                    'deposit_status': 'error'
                })

    return HttpResponseNotAllowed(['POST'])


def wallet_deposit_verify(request: HttpRequest, amount):
    if request.GET.get('Status') == 'OK':
        authority = request.GET.get('Authority')
        merchant_id = config('MERCHANT_ID', '')
        params = {
            'merchant_id': merchant_id,
            'authority': authority,
            'amount': amount
        }

        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        req = requests.post('https://api.zarinpal.com/pg/v4/payment/verify.json', headers=headers, params=params)

        res = None
        try:
            res = req.json()
        except:
            return Http404()

        if res['data']['code'] == 100:
            ref_id = res['data']['ref_id']
            d = DepositTransaction(wallet=request.user.wallet, 
                                   amount=amount,
                                   authority=authority,
                                   ref_id=ref_id,
                                   succeed=True)
            d.save()
            d.apply()
            return render(request, 'shop/checkout_result', {
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
def comments(request: HttpRequest):
    # needs pagination
    # comments = request.user.comments.all()
    state = request.GET.get('state', 'published')

    published = True
    if state != 'published':
        published = False

    paginator = Paginator(
        request.user.comments.filter(published=published), 20)
    pg = request.GET.get('page')
    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, 'user/dashboard/comments.html', {
        'page': page,
        'state': state
    })

@login_required
def messages(request: HttpRequest):
    state = request.GET.get('state', 'unread')
    state_bool = False
    if state == 'read':
        state_bool = True
    messages = request.user.messages.filter(read=state_bool)
    return render(request, 'user/dashboard/messages.html', {
        'messages': messages,
        'state': 'read' if state_bool else 'unread'
    })
    
@login_required
def delete_message(request: HttpRequest, message_id):
    message = get_object_or_404(Message, pk=message_id, user=request.user)
    message.delete()
    return redirect('users:messages')

@login_required
def read_message(request:HttpRequest, message_id):
    message = get_object_or_404(Message, pk=message_id, user=request.user)
    message.read = True
    message.save()
    return redirect('users:messages')

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


@login_required
def favourites(request: HttpRequest):
    # likeds = request.user.favourites
    return render(request, 'user/dashboard/favourites.html', {
        'favourites': 'likeds'
    })


def check_email(request: HttpRequest):
    if request.method == 'POST':
        email_fom = EmailCheckerForm(request.POST)
        status = 'invalid'
        if email_fom.is_valid():
            user = User.objects.filter(
                email=email_fom.cleaned_data['email']).first()
            if not user or user == request.user:
                status = 'valid'
                
        return JsonResponse({
                'status': status
            })

    return HttpResponseNotAllowed(['POST'])


#-------------------------TICKETS-----------------------

@login_required
def create_ticket(request: HttpRequest):
    ticket_types = TicketType.objects.all()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket =  form.save(commit=False)
            ticket.user = request.user
            if request.user.is_staff:
                ticket.repilied = True
            else:
                ticket.repilied = False
            ticket.save()
            return redirect('users:ticket', ticket_id=ticket.id) 
        else:
            return render(request, 'user/dashboard/create_ticket.html', {
                'errors': form.errors
            })
                
    return render(request, 'user/dashboard/create_ticket.html', {
        'types': ticket_types
    })

@login_required
def reply_ticket(request: HttpRequest, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not (ticket.user == request.user or request.user.is_staff):
        return HttpResponseForbidden('you dont have permission to reply ')
    if request.method == 'POST':
        reply_form = TicketReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.ticket = ticket
            reply.save()
            return redirect('users:ticket', ticket_id=ticket.id)
        else:
            return HttpResponse('sfsdfdsf');
    
    return HttpResponseNotAllowed(['POST'])

                
@login_required
def tickets(request: HttpRequest):

    paginator = Paginator(request.user.tickets.all(), 20)
    pg = request.GET.get('page')
    page = None
    try:
        page = paginator.get_page(pg)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return render(request, 'user/dashboard/tickets.html', {
        'page': page,
    })

 
@login_required
def ticket(request: HttpResponse, ticket_id):

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    user = request.user
    if user == ticket.user:
        ticket.seen_by_user = True
    elif user.is_staff:
        ticket.seen_by_intendant = True

    ticket.save()
        
    return render(request, 'user/dashboard/ticket.html', {
        'ticket': ticket
    })

    

