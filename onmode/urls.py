
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

    
from catalogue.views import shop, search, category


urlpatterns = [
    path('', include('index.urls', namespace='index')),
    path('', include('orders.urls', namespace='orders')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('catalogue/', include('catalogue.urls', namespace='catalogue')),
    path('search/', search, name='search' ),
    path('users/', include('users.urls', namespace='users'), ),
    path('<shop_name>/', shop , name='shop'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
