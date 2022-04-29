from django.urls import path

from . import views

app_name='orders'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add', views.add_item, name='add'),
    path('cart/checkout', views.checkout, name='checkout'),
    path('orders/test', views.test, name='test'),
    path('order/<order_code>', views.seller_order, name='order' ),
] 
