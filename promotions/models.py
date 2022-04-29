from asyncio import FastChildWatcher
from pickle import FALSE
from tokenize import String
from urllib.parse import MAX_CACHE_SIZE
from click import edit
from django.db import models
from django.forms import modelformset_factory
from django.utils import timezone
import string
import secrets



class Discount(models.Model):
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(8))
        return code
    
    code = models.CharField(max_length=8, default=generate_code, editable=False)
    percent = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    max_sales_allowed = models.PositiveIntegerField(default=1)
    sales = models.PositiveIntegerField(default=0, editable=False)

    def is_valid(self):
        nw = timezone.now()
        return self.sales < self.max_sales_allowed and (self.start_date < nw < self.end_date)
        
    

class Coupon(models.Model):
    
    #TODO: move it to utils...
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(8))
        return code
    
    
    class TYPE(models.TextChoices):
        AMOUNT = 'AM', 'Amount'
        PERCENT = 'PC', 'Percent'
        
    code = models.CharField(max_length=10, default=generate_code)
    type = models.CharField(max_length=2,
                            choices=TYPE.choices,
                            default=TYPE.PERCENT)
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
        self.save()
    
        
    def apply(self, amount):
        if self.type == self.TYPE.AMOUNT:
            amount -= self.amount
            if amount < 0:
                amount = 0
        else:
            diff = round(amount * (1 - self.percent / 100))
            if diff > self.max_amount:
                diff = self.max_amount
            amount -= diff
        return amount
    
        
        
    
class GiftCard(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_used = models.DateTimeField(null=True)
    
    

