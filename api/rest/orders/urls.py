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

from asyncio import base_events
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartAPIView, UserOrdersVAPIView

router = DefaultRouter()
router.register(r"user/cart", CartAPIView, basename="user-cart")
router.register(r"user/orders", UserOrdersVAPIView, basename="user-orders")
urlpatterns = router.urls
