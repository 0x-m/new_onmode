from atexit import register
from django.contrib import admin
from .models import Order, OrderItem



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'shop', 'final_price', 'tracking_code', 'state', 'issue_return']
    readonly_fields = ['code',]
    list_filter = ['state', 'issue_return']
    search_fields = ['code', 'user__phone_num', 'id']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    @admin.action(description='order code')
    def get_order_code(instance):
        return instance.order.code
    list_display = ['product',get_order_code, 'total_price','has_sales', 'quantity', 'raced']
    list_filters = ['raced',]
    search_fields = ['order__shop__name', 'order__user__phone_num', 'order__code']