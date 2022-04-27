from doctest import FAIL_FAST
import rlcompleter
import secrets 
import string
from django.db import models
from django.utils import timezone

from users.models import Address

class Order(models.Model):
    def generate_code(self):
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(5))
        return code
    
    class STATES(models.TextChoices):
        PENDING = 'pending'
        ACCEPTED = 'accepted'
        SENT = 'sent'
        VERIFIED = 'verified'
        CANCELED = 'canceled'
        FULFILLED = 'fulfilled'
        RETURNED = 'returned'
    
    code = models.CharField(max_length=20, default=generate_code, unique=True)
    user = models.ForeignKey(to='Customer')
    shop = models.ForeignKey(to='Shop')
    state = models.CharField(choices=STATES.choices, default=STATES.PENDING)
    tracking_code = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_fulfilled = models.DateTimeField(null=True)
    issue_return = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=20, blank=True)
    coupon_type = models.CharField(max_length=20, blank=True)
    coupon_percent = models.PositiveIntegerField(default=0)
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.ForeignKey(to=Address, related_name='orders', on_delete=models.SET_NULL, null=True)
    
    @property
    def total_price(self):
        total = 0
        for item in self.items:
            total += item.price
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              related_name='items')

    product = models.ForeignKey(to='Product')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percent = models.PositiveIntegerField(default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(default=0)
    options = models.JSONField(null=True)
    
   
class ReturnRequest(models.Model):
    order = models.ForeignKey(to=Order, related_name='return_requests', on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_fulfilled = models.DateTimeField(null=True)
    description = models.TextField(max_length=5000, blank=True)
    proccessed = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)

class ReturnRequestItem(models.Model):
    retutrn_request = models.ForeignKey(to=ReturnRequest, related_name='items', on_delete=models.CASCADE)
    order_item = models.ForeignKey(to=OrderItem, related_name='returns', on_delete=models.SET_NULL)
    description = models.TextField(max_length=1000)