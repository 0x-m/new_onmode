from gettext import Catalog
from unicodedata import name
from django.urls import path
from . import views
from catalogue import views as catalog

app_name = 'users'
urlpatterns = [
    path('signup/', views.signup , name='signup'),
    path('verify/', views.verify_code, name='verify'),
    path('signout/', views.signout, name='singout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/addresses', views.addresses, name='addresses'),
    path('dashboard/comments', views.comments, name='comments'),
    path('dashboard/favourites', views.favourites, name='favourites'),
    path('dashboard/messages', views.messages, name='messages'),
    path('dashboard/orders', views.orders, name='orders'),
    path('dashboard/wallet', views.wallet, name='wallet'),
    path('dashboard/wallet/deposit', views.wallet_deposit, name='deposit'),
    path('dashboard/wallet/checkout', views.wallet_checkout, name='wallet_checkout'),
    path('dashboard/shop/create-shop', catalog.create_shop_request,name='create-shop' ),
    path('dashboard/shop/edit', catalog.edit_shop, name='edit-shop'),
    path('dashboard/shop/product', catalog.product, name='add-product'),
    path('dashboard/shop/product/edit/<pid>', catalog.product, name='edit-product'),
    path('dashboard/shop/product/options/add/<pid>', catalog.add_option, name='add-option'),
    path('dashboard/shop/product/options/delete/<pid>', catalog.add_option, name='delete-option'),
    path('dashboard/shop/product/delete/<pid>', catalog.delete_product, name='delete-product'),
    path('dashboard/shop/product/photo/add/<pid>', catalog.add_photo, name='add-photo'),
    path('dashboard/shop/product/photo/delete/<pid>', catalog.delete_photo, name='delete-photo'),
    path('dashboard/shop/product/photo/preview/<pid>', catalog.change_preview_photo, name='make-as-preview'),
    # path('dashboard/shop/orders', views.shop_orders, name='shop_orders'),
    # path('dashboard/shop/order', views.shop_order, name='shop_order'),
    path('dashboard/shop/404', views.notfound, name='notfound'),
    # path('dashboard/shop/checkout_result', views.checkout_result, name='checkout_result'),
    # path('dashboard/shop/cart', views.cart, name='cart'),








    

]