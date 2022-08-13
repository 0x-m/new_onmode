from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from apps.catalogue.views import shop, search, category


urlpatterns = [
    # path("", include("apps.index.urls", namespace="index")),
    # path("", include("apps.orders.urls", namespace="orders")),
    # path(
    #     "robots.txt",
    #     TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    # ),
    # path("tinymce/", include("tinymce.urls")),
    # path("admin/", admin.site.urls),
    # path("catalogue/", include("apps.catalogue.urls", namespace="catalogue")),
    # path("search/", search, name="search"),
    # path(
    #     "users/",
    #     include("apps.users.urls", namespace="users"),
    # ),
    # path("<shop_name>/", shop, name="shop"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
