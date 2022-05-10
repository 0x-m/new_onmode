from django.urls import path

from . import views

app_name = 'catalogue'
urlpatterns = [
    path('filter/<shop_name>', views.filter, name='filter'),
    path('collection/<collection_name>', views.collection, name='collection'),
    path('category/<id>', views.category, name='category'),
    path('product/<product_id>/like', views.like, name='like'),
    path('product/comment', views.comment, name='comment'),
    path('product/<product_code>/detail', views.product_detail, name='product_detail'),
    path('shop/check_name/<shop_name>', views.check_shop_name, name='check_shop_name'),
    path('product/add-related/<product_id>/', views.add_related_product, name='add-related'),
    path('product/delete-related/<product_id>', views.delete_related_product, name='delete-related'),


]
