from lib2to3.pgen2.pgen import DFAState
from signal import raise_signal
from tkinter.tix import Tree
from aiohttp import request
from django import forms
from pkg_resources import require
from .models import Order, OrderItem
from catalogue.models import Collection, Product, Shop


class AcceptOrderForm(forms.Form):
    order = forms.IntegerField(required=True)
    shop = forms.IntegerField(required=True)
    
    def clean_order(self):
        id = self.cleaned_data['order']
        try:
            order = Order.objects.get(pk=id)
            return order
        except:
            raise forms.ValidationError('Order does not exist')
    
    def clean_shop(self):
        id = self.cleaned_data['shop']
        try:
            shop = Shop.objects.get(pk=id, active=True)
            return shop
        except:
            raise forms.ValidationError('Shop does not exist')
        
    
    def clean(self, **kwargs):
        shop = self.cleaned_data['shop']
        order = self.cleaned_data['order']
        if order.shop != shop:
            raise forms.ValidationError('order does not belog to the shop')




class AddOrderItemForm(forms.ModelForm):
    # quantity = forms.IntegerField(initial=1, min_value=1)
    # options = forms.JSONField(required=False)
    class Meta:
        model = OrderItem
        fields = ['product', 'collection', 'quantity', 'options']
    # product = forms.ModelChoiceField(queryset=Product.objects.filter(deleted=False))
    # collection = forms.ModelChoiceField(queryset=Collection.objects.all(), required=False)
    
        
    