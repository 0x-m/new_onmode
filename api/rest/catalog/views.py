from urllib import request
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.routers import DefaultRouter
from .permissions import IsOwnerOrAdmin, IsProductSellerOrAdmin, IsSeller, IsOwner

from .serializers import *
from apps.catalogue.models import *
from .permissions import IsSeller, isSellerOrAdmin
from rest_framework.permissions import SAFE_METHODS


class CategoryAPIViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return super().get_permissions()

        return [IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShopAPIViewset(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        # Only Admin can Createor truely Remove a Shop or get a list of all shops.
        if self.action in ["create", "list"]:
            return [IsAdminUser]
        elif self.action in ["retrieve"]:  # Anybody can see a shop page!
            return [AllowAny]
        return [isSellerOrAdmin]  # Owner of the shop can edit the shop.

    def perform_destroy(self, instance):
        if request.user.is_staff:
            return super().perform_destroy(instance)

        instance.deleted = True
        instance.save()


class ProductAPIViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny]
        elif self.action == "list":
            return [IsAdminUser]

        return [IsProductSellerOrAdmin]

    def perform_destroy(self, instance):
        if self.user.is_staff:
            return super().perform_destroy(instance)
        instance.deleted = True
        instance.save()

    # Filtering should be added..


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser]
        elif self.action in ["update", "parial_update", "destroy"]:
            return [IsOwnerOrAdmin]

        return [IsAuthenticated]  # any Authenticatd user can leave a commnent.


class FavouritViewset(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
