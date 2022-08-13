from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        # obj is an instance of Shop
        return obj.owner == request.user


class isSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsProductSellerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.shop.owner == request.user or request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
