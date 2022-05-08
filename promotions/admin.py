
from inspect import classify_class_attrs
from django.contrib import admin
from django.urls import clear_script_prefix

from .models import Coupon, Discount, GiftCard

from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ExportMixin


class GiftResource(ModelResource):
    class Meta:
        model = GiftCard
        fields = ['id', 'user__phone_num', 'amount', 'used', 'date_created', 'date_used', 'start_date', 'end_date']
        exprot_order = ['id', 'user__phone_num', 'amount', 'date_created', 'date_used', 'start_date', 'end_date', 'used']

@admin.register(GiftCard)
class GiftCardAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = GiftResource
    readonly_fields = ['code', 'date_created', 'date_used']
    list_filter = ['date_created', 'date_used', 'used', 'amount']
    
    
    
class DiscountResource(ModelResource):
    class Meta:
        mdoel = Discount
        fields = ['id','code', 'percent', 'start_date', 'end_daate', 'max_amount']
        expor_order = ['id','code', 'percent', 'max_amount', 'start_date', 'end_date']
        
    
@admin.register(Discount)
class DiscountAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = DiscountResource
    list_display = ['percent', 'start_date', 'end_date', 'is_valid']
    readonly_fields = ['code']
    list_filter = ['start_date', 'end_date', 'percent']
    
    
class CouponResource(ModelResource):
    class Meta:
        model = Coupon
        fields = ['id','code','type', 
                  'percent', 'amount', 
                  'max_amount', 'start_date', 'end_date', 
                  'date_created', 'date_used', 'used']
        export_order = ['id','code', 'type', 'percent', 'amount', 'max_amount',
                        'start_date', 'end_date', 'date_created', 'date_used', 
                        'used']
        

@admin.register(Coupon)
class CouponAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CouponResource
    list_display = ['code', 'type', 'amount', 'percent','used']
    list_filter = ['used', 'type', 'date_created', 'date_used', 'percent', 'amount']
    readonly_fields = ['code', 'date_created', 'date_used']
    