from importlib import import_module
from turtle import update
from venv import create
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action

from apps.users.views import comments

from .permissions import IsOwnerOrAdmin, IsProductSellerOrAdmin, IsSeller, IsOwner
from .serializers import *
from apps.catalogue.models import *
from .permissions import IsSeller, isSellerOrAdmin
from rest_framework.response import Response
from rest_framework import status
from apps.catalogue.models import *

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import exceptions as rest_exceptions
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework.backends import DjangoFilterBackend

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes


@extend_schema_view(
    list=extend_schema(
        description="Get the list of all categories",
    ),
    retrieve=extend_schema(
        description="Get category by ID",
    ),
)
class CategoryListAPIView(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("parent",)


@extend_schema_view(
    list=extend_schema(
        description="Get the list of all shops",
    ),
    create=extend_schema("Create a new shop (ADMIN ONLY)"),
    retrieve=extend_schema("Get the shop by id"),
    update=extend_schema("Update the information of a shop (ADMIN OR SHOPKEEPER)"),
)
class ShopAPIViewset(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        # Only Admin can Create or truely Remove a Shop or get a list of all shops.
        if self.action in ["create", "list"]:
            return [IsAdminUser()]

        elif self.action in ["retrieve"]:  # Anybody can see a shop page!
            return [AllowAny()]
        return [isSellerOrAdmin()]  # Owner of the shop can edit the shop.

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            return super().perform_destroy(instance)

        instance.deleted = True
        instance.save()


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def get_user_shop(request: HttpRequest):
    """
    Get the shop (if any) that belongs to the user who made this request.
    """
    try:
        shop = Shop.objects.get(owner=request.user)
        ser = ShopSerializer(shop)
        return Response(ser.data, status=200)

    except Shop.DoesNotExist:
        raise rest_exceptions.NotFound("shop was not found")


@extend_schema_view(
    list=extend_schema(
        description="Get the list of all products (ADMIN ONLY) or all products belongs to the specific shop"
    ),
    create=extend_schema(description="Create a new product for the user's shop"),
)
class ProductAPIViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        shop_pk = self.kwargs.get("shop_pk")
        if shop_pk:
            return Product.objects.filter(shop__id=shop_pk)
        return Product.objects.all()

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return [AllowAny()]
        return [IsProductSellerOrAdmin()]

    def perform_destroy(self, instance):
        if self.user.is_staff:
            return super().perform_destroy(instance)
        instance.deleted = True
        instance.save()


@extend_schema_view(
    list=extend_schema(
        description="Get the list of all comments for the product with the given id."
    ),
    create=extend_schema(
        description="Add a comment for the product with the given id."
    ),
    retrieve=extend_schema(
        description="Get the comment with the given id that belongs to the product with the given product_id"
    ),
    update=extend_schema(
        description="Edit the comment with the given id that belongs to the product with the given product_id"
    ),
    destroy=extend_schema(
        description="Delete the comment with the given id that belongs to the product with the given product_id"
    ),
)
class ProductCommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            product_pk = self.kwargs.get("product_pk")
            comment = Comment.objects.get(
                product__pk=product_pk, user=self.request.user
            )
            return comment
        except Comment.DoesNotExist:
            raise rest_exceptions.NotFound("No commnet with the give id was found.")

    def get_queryset(self):
        product_id = self.kwargs.get("product_pk")
        return Comment.objects.filter(product__id=product_id)

    def get_permissions(self):
        if self.action in ["update", "parial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        elif self.action == "craete":
            return [IsAuthenticated()]
        return [AllowAny()]  # any Authenticatd user can leave a commnent.

    def perform_create(self, serializer):
        product_pk = self.kwargs.get("product_pk")
        serializer.save(user=self.request.user, product__pk=product_pk)


class UserCommentViewset(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        description="Get the list of customers who add the product withe given product_id to their favourite list."
    ),
    create=extend_schema(
        description="Add the product with the product_id which is specified in the body, to the favourite list of the user who made this request"
    ),
    destroy=extend_schema(
        description="Delete the favourite item with the given favourite_id from the favourite list of the user who made this request."
    ),
)
class ProductFavouriteViewset(ModelViewSet):
    serializer_class = FavouriteSerializer
    queryset = Favourite.objects.none()

    def get_permissions(self):
        if self.action != "create":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    retrieve=extend_schema(
        description="Get the favourite item with the give favourite_id that belongs to the currently authenticated user."
    ),
    list=extend_schema(description="Get the favourite list of the user."),
)
class UserFavouriteViewset(ReadOnlyModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
