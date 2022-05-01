from atexit import register
from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['code']
    
admin.site.register(OrderItem)