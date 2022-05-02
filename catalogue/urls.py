from django.urls import path

from . import views

app_name = 'catalogue'
urlpatterns = [
    path('filter/', views.filter, name='filter'),
    path('collection/<collection_name>', views.collection, name='collection'),
    path('product/<product_id>/like', views.like, name='like'),
    path('product/comment', views.comment, name='comment'),
    path('product/<product_code>/detail', views.product_detail, name='product_detail')

]
