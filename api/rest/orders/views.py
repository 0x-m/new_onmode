# Copyright (C) 2022 mohammad
#
# This file is part of Onmode fashoin Shop.
#
# Onmode fashoin Shop is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Onmode fashoin Shop is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Onmode fashoin Shop.  If not, see <http://www.gnu.org/licenses/>.

from ast import expr_context
from curses import REPORT_MOUSE_POSITION
from http.client import ImproperConnectionState
from importlib.machinery import PathFinder
from os import stat
from ssl import create_default_context
from xmlrpc.client import ResponseError
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from apps.orders.models import Order, OrderItem
from apps.users.views import orders
from .permissions import IsOrderItemOwner, IsOrderOwner
from .serializes import CartItemSerializer, OrderItemSerialzier, OrderSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions


# -----------------------------------------
# ------------ Get User orders API --------
# -----------------------------------------
class UserOrdersVAPIView(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, paid=True)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return Order.objects.filter(paid=True, user=self.request.user, pk=pk)


# --------------------------------------------


# ------------------------------------------------
# --------------- CART API -----------------------
# ------------------------------------------------
class CartAPIView(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order_item_id = self.kwargs.get("pk")
        try:
            Order_item = OrderItem.objects.get(
                pk=order_item_id, order__user=self.request.user, order__paid=False
            )
            return Order_item
        except OrderItem.DoesNotExist:
            raise exceptions.NotFound("order item was not found")

    def get_serializer(self, *args, **kwargs):
        if self.action in ["retrieve"]:
            return OrderItemSerialzier(*args, **kwargs)
        elif self.action == "list":
            return OrderSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(paid=False, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        order_item = self.get_object()
        order_item.delete()
        return Response("Order item was deleted", status=200)

    def update(self, request, *args, **kwargs):
        order_item = self.get_object()
        quantity = request.data.get("quantity")
        order_item.quantity = quantity
        order_item.save()
        return Response("item was updated", status=200)


# -----------------------------------------------------------
