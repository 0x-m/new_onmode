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

from apps.users.models import User, Wallet
from rest_framework import serializers


class UserProfileSerlilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "phone_num",
            "email",
            "referral_code",
            "has_shop",
            "consumed_storage",
            "custom_storage_capacity",
            "request_for_shop",
            "request_accepted",
        )
        read_only_fields = [
            "phone_num",
            "referral_code",
            "has_shop",
            "consumed_storage",
            "request_for_shop",
            "request_accepted",
            "custom_storage_capacity",
        ]


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("available", "freezed", "date_last_withdraw")
