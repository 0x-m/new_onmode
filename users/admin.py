from contextlib import nullcontext
from csv import list_dialects
from attr import fields
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from .models import CheckoutRequest, User, Address, Wallet

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
from jalali_date import datetime2jalali, date2jalali
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    password1 = None
    password2 = None
    
    class Meta:
        model = User
        fields = ['phone_num', 'email']

class AddressInline(admin.StackedInline):
    model = Address

class WalletInline(admin.StackedInline):
    model = Wallet
    readonly_fields = ['date_last_withdraw']
    
class UserModelAdmin(UserAdmin):
    
   add_form = UserCreationForm
   add_fieldsets = (
        (None,{
            'fields':('phone_num','email')
        }),
    )
   fieldsets = ((_("Phone Number (Username)"),{
        "fields": ['phone_num',]
        }),
        (_("Other informations"),{
            'fields': ('id','first_name','last_name','gender','email')
        }),
        (_('History'),{
            'fields':('date_joined','last_login',)
        }),
        (_('Privileges'),{
            'fields': ('is_active','is_staff','is_superuser')
        }),
        (_('Groups and Permissions'),{
            'fields': ('groups',),
            
        }),

    )
   ordering = ['phone_num', 'first_name', 'last_name']
   readonly_fields = ['date_joined','last_login','user_code','id']
   list_display = ['phone_num', 'first_name', 'is_active']
   list_editable = ['is_active']
   search_fields = ['phone_num', 'first_name', 'last_name']
   inlines = [WalletInline]
   



admin.site.register(User, UserModelAdmin)

@admin.register(Address)
class AdminAddress(ModelAdmin):
    list_display = ['full_name', 'province', 'city', 'postal_code']
    
@admin.register(CheckoutRequest)
class CheckoutAdmin(ModelAdmin):
    @admin.display(description='customer')
    def customer(instance):
        return instance.wallet.user.phone_num

    list_display = [customer,'amount', 'state', 'date_created']
    fields = [customer, 'merch_card', 'amount', 'call_me', 'state', 'date_created', 'date_proceeded']
    readonly_fields = [customer,'date_created', 'date_proceeded']

   