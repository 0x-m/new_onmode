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
    path('order/accept/', views.accept, name='accept' ),
    path('order/reject/', views.reject, name='reject' ),
    path('order/cancel/', views.cancel, name='cancel' ),
    path('order/tracking_codde/', views.tracking_code, name='tracking_code' ),
    path('order/fulfill/', views.fulfill, name='fulfill' ),
    path('dashboard/orders', views.user_orders, name='user_orders' ),
    path('dashboard/shop/orders', views.shop_orders, name='shop_orders' ),
    path('dashboard/shop/orders/<order_code>/', views.shop_order, name='shop_order' ),
    path('dashbaord/orders/<order_code>', views.user_order, name='user_order' ),
    path('order/<order_id>/verify_payment/', views.verify_payment, name='verify_payment'),
] 
