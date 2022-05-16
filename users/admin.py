
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms


from .models import CheckoutRequest, DepositTransaction, Message, Ticket, TicketReply, TicketType, User, Address, Wallet

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
from jalali_date import datetime2jalali, date2jalali
from django.utils.translation import gettext_lazy as _
from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from import_export.fields import Field




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
            'fields': ('id','first_name','last_name','gender','email', 'has_shop', 'consumed_storage')
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
    
    
class CheckoutResource(ModelResource):
    customer = Field()

    def dehydrate_customer(self, checkout):
        return checkout.wallet.user.phone_num
    
    class Meta:
        mdoel = CheckoutRequest
        fields = ['id' ,'customer','amount','merch_card', 'state', 'date_created', 'date_proceeded']    
        export_order = ['id', 'customer', 
                        'merch_card', 
                        'amount',
                        'wallet__freezed',
                        'wallet_available', 
                        'date_created', 
                        'date_proceeded',]

@admin.register(CheckoutRequest)
class CheckoutAdmin(ExportMixin,ModelAdmin):
    resource_class = CheckoutResource
    @admin.display(description='customer')
    def customer(instance):
        return instance.wallet.user.phone_num

    @admin.display(description='freezed')
    def freezed(instance):
        return instance.wallet.freezed
    
    @admin.display(description='available')
    def available(instance):
        return instance.wallet.available
    
    @admin.display(description='fulfill')
    def fulfill_checkout(model, request, qs):
        for c in qs:
            c.fulfill() #TODO: use update bach for ....
        
    list_display = [customer,'amount','fee',freezed, available, 'state' ,'date_created']
    fields = [customer, 'merch_card', 'amount', 'call_me', 'state', 'date_created', 'date_proceeded']
    readonly_fields = [customer,'date_created', 'date_proceeded']
    actions = [fulfill_checkout]

class DepositResource(ModelResource):
    user = Field()
    
    def dehydrate_user(self, deposit):
        return deposit.wallet.user.phone_num
    
    class Meta:
        model = DepositTransaction
        fields = ['id','user', 'amount', 'date_committed', 'succeed']
        export_order = ['id','user', 'amoutn', 'date_committed', 'succeed']


@admin.register(DepositTransaction)
class DepositAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DepositResource
    fields  = ['id', 'amount', 'date_committed', 'succeed']
    readonly_fields = ['id', 'date_committed']
    


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'title', 'read']
    list_filter = ['type', 'read']
    readonly_fields = ['read']
    

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'title', 'closed']
    list_filte = ['type', 'closed', 'date_created']
    readonly_fields = ['can_reply', 'replied', 'seen_by_user', 'seen_by_intendant']
    

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['title']