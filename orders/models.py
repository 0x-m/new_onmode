
import string
import secrets
from tkinter.tix import Balloon
from django.db import models
from django.utils import timezone
from django.urls import reverse

from promotions.models import Coupon
from users.models import Address


from users.models import User
from catalogue.models import Shop, Product, Collection


class Order(models.Model):
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(5))
        return code
    
    class PAYSOURCE(models.TextChoices):
        WALLET = 'wallet',
        DIRECT = 'direct'

    class STATES(models.TextChoices):
        PENDING = 'pending'
        ACCEPTED = 'accepted'
        REJECTED = 'Rejected'
        VERIFYING = 'verifying',
        NOTVERIFIED = 'notverified'
        SENT = 'sent'
        CANCELED = 'canceled'
        FULFILLED = 'fulfilled'
        RETURNED = 'returned'

    code = models.CharField(
        max_length=20, default=generate_code, editable=False)
    user = models.ForeignKey(
        to=User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    shop = models.ForeignKey(
        to=Shop, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(
        max_length=20, choices=STATES.choices, default=STATES.PENDING)
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
        to=Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    coupon_code = models.CharField(max_length=20, blank=True)
    coupon_type = models.CharField(max_length=20, blank=True)
    coupon_percent = models.PositiveIntegerField(default=0)
    coupon_amount = models.PositiveBigIntegerField(default=0)
    address = models.ForeignKey(
        to=Address, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    ref_id = models.CharField(max_length=255, blank=True)
    authority = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)
    pay_source  = models.CharField(max_length=20, choices=PAYSOURCE.choices, null=True)
    @property
    def quantity(self):
        q = 0
        for item in self.items.all():
            q += item.quantity
        return q

    def set_coupon(self, coupon: Coupon):
        if coupon.used:
            return Exception('coupon was used before')

        self.coupon = coupon
        self.coupon_type = coupon.type
        self.coupon_code = coupon.code
        self.coupon_amount = coupon.amount
        self.coupon_percent = coupon.percent
        self.save()


    @property
    def description(self):
        return  'مبلغ پرداختی:' + str(self.final_price) + '  ' + '\n' + 'گیرنده:' + str(self.address)
        
    def delete_coupon(self):
        if not self.coupon:
            return

        self.coupon = None
        self.coupon_type = ''
        self.coupon_percent = 0
        self.coupon_amount = 0
        self.coupon_code = ''
        self.save()

    @property
    def total(self):
        '''
        total price before applying coupon
        '''
        total = 0
        for item in self.items.all():
            if item.available:
                total += item.total_price
        return total

    @property
    def final_price(self):
        '''
        total price after applying coupon
        '''
        
        total = self.total
        coupon = self.coupon
        if coupon and coupon.is_valid():
            total = coupon.apply(total)
        return total

    @property
    def has_tracking_code(self):
        return self.tracking_code not in [None, '']

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
        # -----------------------

        self.save()

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
        return 'order(' + self.code + ')'

    def __len__(self):
        count = 0
        for item in self.items.all():
            if item.available:
                count += len(item)

        return count
    

    # TODO: use meaningful exceptions...

    def reject(self, msg=''):
        if self.state == self.STATES.PENDING:
            self.state = self.STATES.REJECTED
            self.reject_msg = msg
            # decrease seller freezed and increase buyer available
            self.user.deposit(self.final_price)
            self.shop.owner.wallet.dec_freeze(self.final_price)
            # ----------------------------------------------------
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
        if self.state == self.STATES.ACCEPTED:
            self.tracking_code = code
            self.state = self.STATES.VERIFYING
            self.save()
        else:
            raise Exception('')  # TODO

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
        else:
            raise Exception()

    def cancel(self, msg):
        if self.state == self.STATES.PENDING:
            self.state = self.STATES.CANCELED
            self.cancel_msg = msg
            # back money to buyer
            self.user.deposit(self.final_price)
            self.shop.owner.wallet.dec_freeze(self.final_price)

            self.save()
        else:
            raise Exception()


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              related_name='items')

    product = models.ForeignKey(
        to=Product, related_name='orders', on_delete=models.SET_NULL, null=True)
    price = models.PositiveBigIntegerField(default=0)
    sales_price = models.PositiveBigIntegerField(default=0)
    has_sales = models.BooleanField(default=False)
    final_price = models.PositiveBigIntegerField(
        default=0, help_text='total price after discount')
    discount_code = models.CharField(max_length=8, blank=True, editable=False)
    discount_pecent = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    options = models.JSONField(null=True, blank=True)
    collection = models.ForeignKey(
        to=Collection, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    raced = models.BooleanField(default=False)

    def refresh(self):
        self.price = self.product.price
        self.sales_price = self.product.sales_price
        self.has_sales = self.product.has_sales
        self.final_price = self.product.compute_price(self.collection)
        discount = self.product.get_discount(self.collection)
        if discount:
            self.discount_code = discount.code
            self.discount_pecent = discount.percent
        self.save()

    def is_expired(self):
        return (self.final_price != self.product.compute_price(self.collection))

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
            raise Exception('run out of product')

    def decrement(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()
        if self.quantity == 0:
            # TODO: create a new exceptio derived class...
            raise Exception('this item must be deleted')

    def __len__(self):
        return self.quantity


class ReturnRequest(models.Model):
    order = models.ForeignKey(
        to=Order, related_name='return_requests', on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_fulfilled = models.DateTimeField(null=True)
    description = models.TextField(max_length=5000, blank=True)
    proccessed = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)


class ReturnRequestItem(models.Model):
    retutrn_request = models.ForeignKey(
        to=ReturnRequest, related_name='items', on_delete=models.CASCADE)
    order_item = models.ForeignKey(
        to=OrderItem, related_name='returns', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000)
