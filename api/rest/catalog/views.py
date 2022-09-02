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


class CategoryListAPIView(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AllowAny]


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
    try:
        shop = Shop.objects.get(owner=request.user)
        ser = ShopSerializer(shop)
        return Response(ser.data, status=200)

    except Shop.DoesNotExist:
        raise rest_exceptions.NotFound("shop was not found")


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
            return [AllowAny]
        return [IsProductSellerOrAdmin]

    def perform_destroy(self, instance):
        if self.user.is_staff:
            return super().perform_destroy(instance)
        instance.deleted = True
        instance.save()


class ProductCommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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


class ProductFavouriteViewset(ModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action != "create":
            return [IsAdminUser()]

    def perform_create(self, serializer):
        product_pk = self.kwargs.get("product_pk")
        serializer.save(product__pk=product_pk, user=self.request.user)


class UserFavouriteViewset(ReadOnlyModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
