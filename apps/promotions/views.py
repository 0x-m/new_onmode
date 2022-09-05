"""

author: hamze ghaedi (github: 0x-m)

"""


from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    JsonResponse,
)
from django.shortcuts import get_object_or_404

from .models import GiftCard


@login_required
def appyl_gift(request: HttpRequest):
    if request.method == "POST":
        gift_code = request.POST.get("gift_code")
        giftcard = get_object_or_404(GiftCard, code=gift_code)
        try:
            giftcard.apply(request.user)
            return JsonResponse({"status": "applied"})
        except Exception:
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed(["POST"])
