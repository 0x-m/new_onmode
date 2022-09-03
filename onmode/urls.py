from http.client import ImproperConnectionState
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from apps.catalogue.views import shop, search, category

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularAPIView,
)

urlpatterns = [
    path("", include("apps.index.urls", namespace="index")),
    path("", include("apps.orders.urls", namespace="orders")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("catalogue/", include("apps.catalogue.urls", namespace="catalogue")),
    path("search/", search, name="search"),
    path(
        "users/",
        include("apps.users.urls", namespace="users"),
    ),
    path("<shop_name>/", shop, name="shop"),
    path("api/v1/", include("api.rest.catalog.urls")),
    path("api/v1/", include("api.rest.orders.urls")),
    path("api/v1/", include("api.rest.users.urls")),
    path("api/v1/user/registration", include("dj_rest_auth.registration.urls")),
    path("api/v1/token/", TokenObtainPairView.as_view(), "token-obtain"),
    path("api/v1/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/token/verify", TokenVerifyView.as_view(), name="token-verify"),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/v1/docs/swagger",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs-swagger",
    ),
    path(
        "api/v1/docs/redoc",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-docs-redoc",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
