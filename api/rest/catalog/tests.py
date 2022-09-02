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
from django.urls import reverse
from apps.catalogue.models import Category


class TestCategoryListAPI(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cat = Category.objects.create(name="books")
        sub_cat = Category.objects.create(name="sci-fi", parent=cat)
        return super().setUpTestData()

    def test_get_categories(self):
        resp = self.client.get("/api/v1/categories/")
        print(resp.json())


class TestFavouriteAPI(APITestCase):
    def test_get_user_favourites(self):
        pass

    def test_get_product_favourites(self):
        pass

    def test_add_product_to_favourites(self):
        pass

    def test_remove_product_from_favourites(self):
        pass


class TestCommentAPI(APITestCase):
    def test_get_user_comments(self):
        pass

    def test_get_product_comments(self):
        pass

    def test_leave_comment_for_a_product(self):
        pass
