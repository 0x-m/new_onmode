from typing import Counter
from django.contrib import admin

from .models import Coupon, Discount, GiftCard

admin.site.register(Discount)
admin.site.register(Coupon)
admin.site.register(GiftCard)