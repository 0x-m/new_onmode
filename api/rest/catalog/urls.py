from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryListAPIView,
    ProductCommentViewset,
    ProductFavouriteViewset,
    ShopAPIViewset,
    UserCommentViewset,
    UserFavouriteViewset,
    get_user_shop,
)

router = DefaultRouter()
router.register(r"categories", CategoryListAPIView, basename="categories")
router.register(r"shops", ShopAPIViewset, basename="shops")
router.register(
    r"products/<int:product_pk>/comments",
    ProductCommentViewset,
    basename="product-comments",
)
router.register(
    r"products/<int:product_pk>/favourites",
    ProductFavouriteViewset,
    basename="product-favourites",
)
router.register(r"user/comments", UserCommentViewset, basename="user-comments")
router.register(
    r"user/favourites", UserFavouriteViewset, basename="use-favourites"
)


urlpatterns = [
    path("", include(router.urls)),
    path("user/shop/", get_user_shop, name="user-shop"),
    # path(
    #     "/products/<product_pk>/comments/",
    #     ProductCommentViewset.as_view(),
    #     name="product-comments",
    # ),
    # path(
    #     "/products/<product_pk>/favourites/",
    #     ProductFavouriteViewset.as_view(),
    #     name="product-favourites",
    # ),
    # path("/user/comments/", UserCommentViewset.as_view(), name="user-comments"),
    # path("/user/favourites", UserFavouriteViewset.as_view(), name="user-favourites"),
]
