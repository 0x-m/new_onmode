from xmlrpc.server import resolve_dotted_attribute
from django.contrib import admin
from .models import Order, OrderItem, WalletAlternation
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field


class OrderResource(resources.ModelResource):
    shop = Field(attribute='shop__name', column_name='shop')
    user = Field(attribute='user__phone_num', column_name='user')
    final_price = Field()
    
    def dehydrate_final_price(self, order):
        return order.final_price
    
    class Meta:
        model = Order
        fields = ['id', 'code', 
                  'final_price'
                  , 'state', 'tracking_code', 
                  'coupon_code', 'coupon_type', 
                  'coupon_amount', 'coupon_percent', 
                  'ref_id', 'authority', 'paid', 
                  'pay_source', 'date_created', 
                  'date_fulfilled', 'issue_return' ]
        export_order = [
            'id', 'code',
            'shop', 'user',
            'final_price', 'state',
            'tracking_code', 'coupon_type',
            'coupon_amount', 'coupon_percent',
            'ref_id', 'authority', 'paid', 'pay_source',
            'date_created', 'date_fulfilled', 'issue_return'
        ]

@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    
    resource_class = OrderResource

    @admin.action(description='accept order as seller')
    def accept(model, request, qs):
        for order in qs:
            order.accept()
    
    @admin.action(description='reject order as seller')
    def reject(model, request, qs):
        for order in qs:
            order.reject()

    @admin.action(description='cancel order as customer')    
    def cancel(model, request, qs):
        for order in qs:
            order.cancel()
 
    @admin.action(description='verify tracking code')   
    def verify_tracking_code(model, request, qs):
        for order in qs:
            order.verify()

    @admin.action(description='reject tracking code')
    def reject_tracking_code(model, request, qs):
        for order in qs:
            order.refuse()

    @admin.action(description='fulfill order as customer')
    def fulfill(model, request, qs):
        for order in qs:
            order.fulfill()
    
    @admin.action(description='mark order as returned')
    def mark_returned(model, request, qs):
        for order in qs:
            order.make_returned()

    @admin.action(description='back to pending state')
    def mark_pending(model, request, qs):
        for order in qs:
            order.make_pending()


    
    list_display = ['user', 'shop', 'final_price', 'tracking_code', 'state', 'issue_return']
    readonly_fields = ['code','state']
    list_filter = ['state', 'issue_return', 'date_created', 'date_fulfilled']
    search_fields = ['code', 'user__phone_num', 'id']
    actions = [accept, reject, 
               cancel, fulfill, 
               verify_tracking_code, 
               reject_tracking_code, mark_returned, 
               mark_pending]
    
    

class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'prod_name', 'prod_en_name', 'price', 'sales_price',
                  'has_sales','final_price','qunatity', 
                  'discount_code', 'discount_percent', 
                  'options', 'collection__name', 'raced' ]   
        
         

@admin.register(OrderItem)
class OrderItemAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderItemResource
    @admin.action(description='order code')
    def get_order_code(instance):
        return instance.order.code
    list_display = ['product',get_order_code, 'total_price','has_sales', 'quantity', 'raced']
    list_filters = ['raced',]
    search_fields = ['order__shop__name', 'order__user__phone_num', 'order__code']

@admin.register(WalletAlternation)
class AlternationAdmin(admin.ModelAdmin):

    @admin.action(description='creditor freezed')
    def get_freezed(instance):
        if instance.creditor:
            return instance.creditor.wallet.freezed
        else:
            return 0
        
        
        
    
    @admin.action(description='creditor available')
    def get_available(instance):
        if instance.creditor:
            return instance.creditor.wallet.available
        else:
            return 0

    @admin.action(description='apply alternation')
    def alter(model, request, qs):
        for item in qs:
            item.apply(request.user)        
        

    list_display = ['id','creditor', 
                    'debtor', 
                    get_freezed, 
                    get_available,
                    'succeed']
    readonly_fields = ['id','intendant','date_created' ]
    fields = ['id', 'intendant','amount', ('creditor', 'creditor_balance_type'),
              ('debtor', 'debtor_balance_type'), 'date_created']
    actions = [alter]
    raw_id_fields = ['creditor', 'debtor']