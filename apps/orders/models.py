import string
import secrets
from django.db import models
from django.utils import timezone
from apps.promotions.models import Coupon
from apps.users.models import Address
from apps.users.models import User
from apps.catalogue.models import Shop, Product, Collection
from decouple import config
from ippanel import Client
from django.db.models.signals import post_save

SEL_API_KEY = config("SELLER_SMS_API_KEY")
CUS_API_KEY = config("CUSTOMER_SMS_API_KEY")
cus_sms_client = Client(CUS_API_KEY)
sel_sms_client = Client(SEL_API_KEY)

# --------------helper functinos-----------------
def send_notification(client: Client, pattern, values, phone_no):
    pattern_code = config(pattern)
    num = config("SMS_NUMBER")
    is_sent = client.send_pattern(pattern_code, num, phone_no, values)
    return is_sent


# -----------------------------------------------


class Order(models.Model):
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = "".join(secrets.choice(alphabet) for _ in range(5))
        return code

    class PAYSOURCE(models.TextChoices):
        WALLET = ("wallet",)
        DIRECT = "direct"

    class STATES(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "Rejected"
        VERIFYING = ("verifying",)
        NOTVERIFIED = "notverified"
        SENT = "sent"
        CANCELED = "canceled"
        FULFILLED = "fulfilled"
        RETURNED = "returned"

    code = models.CharField(
        max_length=20, default=generate_code, editable=False, db_index=True
    )
    user = models.ForeignKey(
        to=User, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    shop = models.ForeignKey(
        to=Shop, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    state = models.CharField(
        max_length=20, choices=STATES.choices, default=STATES.PENDING
    )
    reject_msg = models.TextField(max_length=2000, blank=True)
    order_msg = models.TextField(max_length=2000, blank=True)
    invalid_tracking_code_msg = models.TextField(max_length=2000, blank=True)
    tracking_code = models.CharField(max_length=20, blank=True)
    tracking_code_msg = models.CharField(max_length=255, blank=True)
    cancel_msg = models.TextField(max_length=2000, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_fulfilled = models.DateTimeField(null=True, blank=True)
    issue_return = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        to=Coupon, on_delete=models.SET_NULL, null=True, blank=True
    )
    coupon_code = models.CharField(max_length=20, blank=True)
    coupon_type = models.CharField(max_length=20, blank=True)
    coupon_percent = models.PositiveIntegerField(default=0)
    coupon_amount = models.PositiveBigIntegerField(default=0)
    address = models.ForeignKey(
        to=Address,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ref_id = models.CharField(max_length=255, blank=True, db_index=True)
    authority = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)
    pay_source = models.CharField(max_length=20, choices=PAYSOURCE.choices, null=True)

    @property
    def quantity(self):
        q = 0
        for item in self.items.all():
            q += item.quantity
        return q

    def set_coupon(self, coupon: Coupon):
        if coupon.used:
            return Exception("coupon was used before")

        self.coupon = coupon
        self.coupon_type = coupon.type
        self.coupon_code = coupon.code
        self.coupon_amount = coupon.amount
        self.coupon_percent = coupon.percent
        self.save()

    @property
    def description(self):
        return (
            "مبلغ پرداختی:"
            + str(self.final_price)
            + "  "
            + "\n"
            + "گیرنده:"
            + str(self.address)
        )

    def delete_coupon(self):
        if not self.coupon:
            return

        self.coupon = None
        self.coupon_type = ""
        self.coupon_percent = 0
        self.coupon_amount = 0
        self.coupon_code = ""
        self.save()

    @property
    def total(self):
        """
        total price before applying coupon
        """
        total = 0
        for item in self.items.all():
            if item.available:
                total += item.total_price
        return total

    @property
    def final_price(self):
        """
        total price after applying coupon
        """

        total = self.total
        coupon = self.coupon
        if coupon:
            if coupon.is_valid():
                total = coupon.apply(total)
        total += self.get_shipping_cost()
        return total

    @property
    def has_tracking_code(self):
        return self.tracking_code not in [None, ""]

    @property
    def quantity(self):
        count = 0
        for item in self.items.all():
            count += item.quantity
        return count

    def pay(self, ref_id, authority):
        amount = self.final_price
        self.user.wallet.withdraw(amount)
        self.shop.owner.wallet.inc_freeze(amount)

        if self.coupon:
            self.coupon.set_used()

        self.ref_id = ref_id
        self.authority = authority
        self.paid = True

        # race condition-----------
        for item in self.items.all():
            if not item.product.has_quantity(item.quantity):
                item.raced = True
                item.product.force__dec_quantity(item.product.quantity)
            else:
                item.product.dec_quantity(item.quantity)
            # item.product.stats.inc_sales()
        # -----------------------
        self.save()

        # sms to shopkeeper----------------

        # ---------------------------------

    @property
    def is_expired(self):
        for item in self.items.all():
            if item.is_expired():
                return True

    def get_shipping_cost(self):
        shipping_cost = 0
        c = 0
        for item in self.items.all():
            cost = item.get_shipping_cost()
            if cost != 0:
                c += 1
                shipping_cost += cost
            if c != 0:
                shipping_cost //= c
        return shipping_cost

    def refresh(self):
        for item in self.items.all():
            if item.is_expired():
                item.refresh()

    def accept(self):
        if self.state == self.STATES.PENDING:
            self.state = self.STATES.ACCEPTED
            self.save()
        else:
            raise Exception()

    def __str__(self) -> str:
        return "order(" + self.code + ")"

    def __len__(self):
        count = 0
        for item in self.items.all():
            if item.available:
                count += len(item)

        return count

    # TODO: use meaningful exceptions...

    def reject(self, msg=""):
        if self.state == self.STATES.PENDING:
            self.state = self.STATES.REJECTED
            self.reject_msg = msg
            # decrease seller freezed and increase buyer available
            self.user.wallet.deposit(self.final_price)
            self.shop.owner.wallet.dec_freeze(self.final_price)
            # ----------------------------------------------------
            # inform customer------------------------
            try:
                resp = send_notification(
                    cus_sms_client,
                    "ORDER_REJECTED_SMS_CODE",
                    {"name": self.user.first_name, "id": self.code},
                    self.user.phone_num,
                )
                print("reject sms state:", resp, "------------------------")
            except Exception as e:
                print(f"reject sms faild {e}")

            self.save()
        else:
            raise Exception()

    def fulfill(self):
        if self.state == self.STATES.SENT and self.verified:
            self.state = self.STATES.FULFILLED
            # move seller freezed to available and remove buyer freezed
            self.shop.owner.wallet.release(self.final_price)
            self.save()
        else:
            raise Exception()

    def set_tracking_code(self, code):
        if self.state in [self.STATES.ACCEPTED, self.STATES.NOTVERIFIED]:
            self.tracking_code = code
            self.state = self.STATES.VERIFYING
            self.save()
        else:
            raise Exception("")  # TODO

    def verify(self):
        if self.state == self.STATES.VERIFYING:
            self.state = self.STATES.SENT
            self.verified = True
            self.save()
        else:
            raise Exception()

    def refuse(self):
        if self.state == self.STATES.VERIFYING:
            self.state = self.STATES.NOTVERIFIED
            self.save()
            # ------------inform seller--------------
            try:
                send_notification(
                    sel_sms_client,
                    "ORDER_NOT_VERIFIED_SMS_CODE",
                    {
                        "name": self.shop.owner.first_name,
                        "id": self.code,
                    },
                    self.shop.owner.phone_num,
                )
            except:
                pass
        else:
            raise Exception()

    def cancel(self, msg=""):
        if self.state == self.STATES.PENDING:
            self.state = self.STATES.CANCELED
            self.cancel_msg = msg
            # back money to buyer
            self.user.deposit(self.final_price)
            self.shop.owner.wallet.dec_freeze(self.final_price)
            self.save()
            # ------------inform seller--------------
            try:
                send_notification(
                    sel_sms_client,
                    "ORDER_CANCELED_SMS_CODE",
                    {
                        "name": self.shop.owner.first_name,
                        "id": self.code,
                    },
                    self.user.phone_num,
                )
            except:
                pass

        else:
            raise Exception()

    def make_returned(self):
        self.state = self.STATES.RETURNED
        self.save()

    def make_pending(self):
        self.state = self.STATES.PENDING
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        to=Product, related_name="orders", on_delete=models.SET_NULL, null=True
    )
    prod_name = models.CharField(max_length=255, blank=True)
    prod_en_name = models.CharField(max_length=255, blank=True)
    price = models.PositiveBigIntegerField(default=0)
    sales_price = models.PositiveBigIntegerField(default=0)
    has_sales = models.BooleanField(default=False)
    final_price = models.PositiveBigIntegerField(
        default=0, help_text="total price after discount"
    )
    discount_code = models.CharField(max_length=8, blank=True, editable=False)
    discount_pecent = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    options = models.JSONField(null=True, blank=True)
    free_shipping = models.BooleanField(default=False)
    shipping_cost = models.PositiveBigIntegerField(default=0)
    collection = models.ForeignKey(
        to=Collection,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    raced = models.BooleanField(default=False)

    def refresh(self):
        self.price = self.product.price
        self.prod_name = self.product.name
        self.prod_en_name = self.product.en_name
        self.sales_price = self.product.sales_price
        self.has_sales = self.product.has_sales
        self.final_price = self.product.compute_price(self.collection)
        self.free_shipping = self.product.free_shipping
        self.shipping_cost = self.product.get_shipping_cost
        discount = self.product.get_discount(self.collection)
        if discount:
            self.discount_code = discount.code
            self.discount_pecent = discount.percent
        self.save()

    def is_expired(self):
        return self.final_price != self.product.compute_price(self.collection)

    @property
    def available(self):
        return self.product.has_quantity(self.quantity)

    @property
    def total_price(self):
        return self.quantity * self.final_price

    def increment(self):
        if self.product.has_quantity(self.quantity + 1):
            self.quantity += 1
            self.save()
        else:
            raise Exception("run out of product")

    def decrement(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()
        if self.quantity == 0:
            # TODO: create a new exceptio derived class...
            raise Exception("this item must be deleted")

    def __len__(self):
        return self.quantity

    def get_shipping_cost(self):
        if self.free_shipping:
            return 0
        else:
            return self.shipping_cost


class WalletAlternation(models.Model):
    intendant = models.ForeignKey(
        to=User,
        related_name="alternations",
        on_delete=models.CASCADE,
        null=True,
        editable=False,
    )
    creditor = models.ForeignKey(
        to=User,
        related_name="buyalternation",
        on_delete=models.CASCADE,
        help_text="...lends money",
        null=True,
        blank=True,
    )
    debtor = models.ForeignKey(
        to=User,
        related_name="sellalternation",
        on_delete=models.CASCADE,
        help_text="... borrows money",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(default=0, help_text="tomans")
    succeed = models.BooleanField(default=False, editable=False)
    creditor_balance_type = models.CharField(
        max_length=20,
        choices=[("freezed", "freezed"), ("available", "available")],
        default="freezed",
    )
    debtor_balance_type = models.CharField(
        max_length=20,
        choices=[("freezed", "freezed"), ("available", "available")],
        default="freezed",
    )

    description = models.TextField(max_length=5000, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def apply(self, intendant: User):
        if self.succeed:
            return
        res = True
        if self.creditor:
            if self.creditor_balance_type == "freezed":
                res = self.creditor.wallet.dec_freezed(self.amount)
            elif self.creditor_balance_type == "available":
                res = self.creditor.wallet.withdraw(self.amount)
            if not res:
                return False

        if self.debtor:
            if self.debtor_balance_type == "freezed":
                self.debtor.wallet.inc_freezed(self.amount)
            elif self.debtor_balance_type == "available":
                self.debtor.wallet.deposit(self.amount)

        self.intendant = intendant
        self.succeed = True
        self.save()
        return True
