from django.urls import path

from . import views


app_name = 'cart'
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<pid>', views.add_item, name='add'),
    path('delete/<pid>', views.delete_item, name='delete'),
    path('increment/<pid>', views.increment_item, name='increment'),
    path('decrement/<pid>', views.decrement_item, name='decrement'),
    path('<shop_name>/checkout/', views.checkout, name='checkout'),

]