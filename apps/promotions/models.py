from django.db import models
from django.utils import timezone
import string
import secrets
from apps.users.models import User


class Coupon(models.Model):

    # TODO: move it to utils...
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = "".join(secrets.choice(alphabet) for _ in range(8))
        return code

    class TYPE(models.TextChoices):
        AMOUNT = "AM", "Amount"
        PERCENT = "PC", "Percent"

    code = models.CharField(max_length=10, default=generate_code)
    type = models.CharField(max_length=2, choices=TYPE.choices, default=TYPE.PERCENT)
    percent = models.PositiveIntegerField(default=0)
    amount = models.PositiveBigIntegerField(default=0)
    max_amount = models.PositiveBigIntegerField(default=10000)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_used = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        nw = timezone.now()
        return self.start_date < nw < self.end_date and not self.used

    def set_used(self):
        self.used = True
        self.date_used = timezone.now()
        self.save()

    def apply(self, amount):
        if self.type == self.TYPE.AMOUNT:
            amount -= self.amount
            if amount < 0:
                amount = 0
        else:
            diff = round(amount * (self.percent / 100))
            if diff > self.max_amount:
                diff = self.max_amount
            amount -= diff
        return amount

    def __str__(self) -> str:
        return self.code


class GiftCard(models.Model):
    # TODO: move it to utils...
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = "".join(secrets.choice(alphabet) for _ in range(8))
        return "gift_" + code

    user = models.ForeignKey(
        to=User,
        related_name="gifts",
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_used = models.DateTimeField(null=True, blank=True, editable=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    code = models.CharField(max_length=15, default=generate_code, editable=False)

    def apply(self, user: User):
        if self.is_valid():
            self.user = user
            user.wallet.deposit(self.amount)
            self.date_used = timezone.now()
            self.used = True
            self.save()
        else:
            raise Exception()  # TODO: use conceptual exception...

    def is_valid(self):
        nw = timezone.now()
        return (not self.used) and (self.start_date < nw < self.end_date)

    def __str__(self) -> str:
        return self.code
