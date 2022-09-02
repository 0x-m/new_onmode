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

from dataclasses import field, fields
from pkgutil import ImpImporter
from pydoc import ModuleScanner
from time import clock_settime
from tkinter.messagebox import RETRY
from wsgiref import validate
from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class OrderItemSerialzier(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "prod_name",
            "price",
            "sales_price",
            "final_price",
            "discount_code",
            "quantity",
            "options",
            "free_shipping",
            "collection",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerialzier(many=True)

    class Meta:
        model = Order
        fields = (
            "code",
            "shop",
            "state",
            "reject_msg",
            "order_msg",
            "tracking_code",
            "invalid_tracking_code_msg",
            "cancel_msg",
            "verified",
            "date_created",
            "coupon_code",
            "date_fulfilled",
            "coupon_type",
            "ref_id",
            "authority",
            "paid",
            "pay_source",
            "items",
        )


class CartItemSerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value > 0:
            return value
        return serializers.ValidationError("quantity must be greather than zero")

    def save(self, **kwargs):
        order = Order.objects.get_or_create(
            shop_id=self.validated_data.get("shop_id"),
            user=kwargs.get("user"),
            paid=False,
        )
        order_item, created = OrderItem.objects.update_or_create(
            order=order,
            product_id=self.validated_data.get("product_id"),
            quantity=self.validated_data["quantity"],
        )
        print("here")

        order_item.refresh()
        return order_item
