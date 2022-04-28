from django.http import Http404, HttpRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import AcceptOrderForm

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


def tarcking_code(request: HttpRequest):
    pass



def reject(request: HttpRequest):
    pass


def canceled(request: HttpRequest):
    pass


def fulfilled(request: HttpRequest):
    pass

