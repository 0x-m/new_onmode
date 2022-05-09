from pyexpat import model
from attr import fields
from django import forms
from django.core.validators import RegexValidator

#from catalog.models import Product
#from .models import Comment
from .models import Address, CheckoutRequest, TicketReply, User, Ticket

class SignUpForm(forms.Form):
    phone_num = forms.CharField(max_length=11,
                                validators=[
                                    RegexValidator('^09[0-9]{9}$')
                                ])
    redirect_url = forms.URLField(required=False)

class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=5)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender']
        

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone_number', 'province', 'city', 'town', 'description', 'postal_code']
        
        

        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutRequest
        fields = ['merch_card', 'call_me', 'amount']


# class CommentForm(forms.ModelForm):
#     product = forms.IntegerField(widget=forms.HiddenInput, required=True)

#     class Meta:
#         model = Comment
#         fields = ['title', 'body', 'rate']
        
#     def clean_product_id(self):
#         pid = self.data.get('product', None)
#         if pid:
#             try:
#                 product = Product.objects.get(pk=pid)
#                 return product
#             except Product.DoesNotExist:
#                 raise forms.ValidationError('Product does not exists.')
    


class EmailCheckerForm(forms.Form):
    email = forms.EmailInput()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields  = ['type', 'title', 'body']
        
        
class TicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ['body',]
        