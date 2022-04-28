from signal import raise_signal
from django import forms
from .models import Order
from catalogue.models import Shop

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
        