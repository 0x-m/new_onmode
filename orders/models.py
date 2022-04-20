from django.db import models
from django.forms import modelformset_factory

class ShippingAddress(models.Model):
    pass

class Order(models.Model):
    class STATES(models.TextChoices):
        PENDING = ''
        ACCEPTED = ''
        CANCELED = ''
        SENT = ''
        FULFILLED = ''
        RETURNED = ''
        
    customer = models.ForeignKey(to='Customer')
    shop = models.ForeignKey(to='Shop')
    tracking_code = models.CharField(max_length=20, blank=True, null=True)
    date_created = ''
    date_fulfilled = ''
    returned_cause = ''
    address = ''
    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              related_name='items')

    product = models.ForeignKey(to='Product')
    price = models.DecimalField()
    sales_price = models.DecimalField()
    discounted_price = models.DecimalField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField()
    attributes = models.JSONField()
    message = models.TextField()
    
    
class ShippingMethod(models.Model):
    pass

class Shipping(models.Model):
    pass 