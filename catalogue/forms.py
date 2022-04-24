from calendar import c
from pyexpat import model
from xml.dom import ValidationErr
from attr import fields
from django import forms

from .models import CreateShopRequest, Product, Shop
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from . import models


#TODO: move reserved_words to the utils..or settings
reserved_words = [
    'admin',
    'dashboard',
    'user', 
    'users',
    'catalog', 
    'catalogue',
    'discount',
    'promotion',
    'order',
    'orders',
    'payment',    
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'en_name',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'sku',
            'price',
            'quantity',
            'stock_low_threshold',
            'free_shipping',
            'sold_individually',
            'has_sales',
            'sales_price',
            'shipping_cost',
            'description',
            'attributes',
            
        ]
    

        
  
        
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'meta_title' , 
            'meta_description', 
            'address_description',
            'phone',
        ]

class CreateShopForm(forms.ModelForm):
    class Meta:
        model = CreateShopRequest
        fields = ['title', 'name']
    
    def clean_name(self):
        name: str = self.cleaned_data['name']

        # name should not include any punctuations
        if not name.isidentifier():
            return ValidationErr(msg='invalid name', code='invalid')
        
        if name in reserved_words:
            return ValidationErr(msg='the name is reserved for onmode system', 
                                 code='reserved_words')
        return name
        
        
        