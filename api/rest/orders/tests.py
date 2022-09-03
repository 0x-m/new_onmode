# Copyright (C) 2022 Hamze(mohammad) ghaedi
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


from rest_framework.test import APITestCase

from apps.users.models import User
from apps.orders.models import Order, OrderItem
from apps.catalogue.models import Shop, Product


class TestCartAPI(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(phone_num="099112121414", has_shop=True)
        cls.shop = Shop.objects.create(name="sss", owner=cls.user)
        cls.order = Order.objects.create(user=cls.user, shop=cls.shop)
        cls.product = Product.objects.create(shop=cls.shop, name="nn")

    def test_add_item_to_cart(self):
        self.client.force_login(self.user)
        print(self.user)
        resp = self.client.post(
            "/api/v1/user/cart/", {"product_id": 1, "shop_id": 1, "quantity": 2}
        )
        print(resp.content)

    def test_remove_item_from_cart(self):
        pass


# class TestUserOrderAPI(APITestCase):
#     def test_get_all_orders(self):
#         resp = self.client.get("/api/v1/orders/")
