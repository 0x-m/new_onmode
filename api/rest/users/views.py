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

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions
from .serializers import UserProfileSerlilizer, WalletSerializer

from apps.users.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    retrieve=extend_schema(description="Get the user profile information."),
    update=extend_schema(description="Update the user profile information."),
)
class UserProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerlilizer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class WalletAPIView(RetrieveAPIView):
    """
    Get the user wallet information.
    """

    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet
