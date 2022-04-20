from unicodedata import name
from django.urls import path
from . import views

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
    path('dashboard/shop/about', views.about_shop, name='about_shop'),
    path('dashboard/shop/orders', views.shop_orders, name='shop_orders'),
    path('dashboard/shop/order', views.shop_order, name='shop_order'),




    

]