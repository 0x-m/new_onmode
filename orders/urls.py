from django.urls import path

from . import views

app_name='orders'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add', views.add_item, name='add'),
    path('cart/delete/<order_item_id>', views.delete_item, name='delete'),
    path('cart/increment/<order_item_id>', views.increment, name='increment'),
    path('cart/decrement/<order_item_id>', views.decrement, name='decrement'),
    path('cart/coupon/add', views.set_coupon, name='add_coupon'),
    path('cart/coupon/delete', views.delete_coupon, name='delete_coupon'),
    path('cart/refresh', views.refresh_order, name='refresh'),
    path('cart/checkout/<shop_name>', views.checkout, name='checkout'),
    path('orders/test', views.test, name='test'),
    path('order/<order_code>', views.seller_order, name='order' ),
] 
