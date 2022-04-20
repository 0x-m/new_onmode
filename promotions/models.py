from django.db import models

class Discount(models.Model):
    percent = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def is_valid(self):
        pass
    

class Coupon(models.Model):
    class TYPE(models.TextChoices):
        AMOUNT = 'AM', 'Amount'
        PERCENT = 'PC', 'Percent'
        
    code = models.CharField(max_length=10)
    type = models.CharField(max_length=2,
                            choices=TYPE.choices,
                            default=TYPE.PERCENT)
    percent = models.PositiveIntegerField(default=0)
    amount = models.DecimalField()
    threshold = models.DecimalField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    def isValid(self):
        pass
    
    def refresh(self, day=1):
        pass
    
    def make_used(self):
        pass
    
    
    

