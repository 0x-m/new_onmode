from pyexpat import model
from attr import fields
from django import forms

from .models import Product, Shop
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



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
            'shipping_cost',
            'description',
            'attributes',
            'options',
        ]
        
  
        
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'owmer', 
            'name', 
            'meta_title' , 
            'meta_description', 
            'meta_keywords',
            'address',
            'phone',
        ]
