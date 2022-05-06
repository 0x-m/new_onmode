from csv import list_dialects
from typing import Counter
from django.contrib import admin

from .models import Coupon, Discount, GiftCard



@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    readonly_fields = ['code', 'date_created', 'date_used']
    
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code','percent', 'start_date', 'end_date', 'is_valid']
    readonly_fields = ['code']
    list_filter = ['start_date', 'end_date']
    
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'type', 'amount', 'percent','used']
    list_filter = ['used', 'type']
    readonly_fields = ['code', 'date_created', 'date_used']
    