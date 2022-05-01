from django.urls import path

from . import views

app_name = 'catalogue'
urlpatterns = [
    path('filter/', views.filter, name='filter'),
    path('collection/<collection_name>', views.collection, name='collection'),
    path('product/<product_id>/like', views.like, name='like'),
    path('product/<product_id>/comment', views.comment, name='comment')

]
