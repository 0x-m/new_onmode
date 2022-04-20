from asyncio import FastChildWatcher
from decimal import Decimal
from secrets import choice
from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.forms import modelformset_factory

# from catalog.models import Product

class CustomUserManager(UserManager):
    def create_superuser(self, phone_no, email, password: str):
        u = self.model(phone_no=phone_no, email=self.normalize_email(email))
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        
        
class User(AbstractUser):
    username = None

    email = models.EmailField()
    phone_num = models.CharField(max_length=11, 
                                 validators=[
                                    RegexValidator('^09[0-9]{9}$')
                                     ], unique=True)
    gender = models.CharField(max_length=10,choices=[('men', 'men'),('womamn', 'woman')])
    user_code = models.CharField(max_length=20)
    referral_code = models.CharField(max_length=20, blank=True, null=True)
    request_for_shop = models.BooleanField(default=False)
    request_accepted = models.BooleanField(default=False)
    has_shop = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone_num'
    
    objects = CustomUserManager()
    has_password = models.BooleanField(default=False)
    


class Address(models.Model):
    user = models.OneToOneField(to=User, related_name='addresses', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    postal_code = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.province + '/' + self.city + '/' + self.town
    
    
    
class Wallet(models.Model):
    user = models.OneToOneField(to=User, related_name='wallet')
    available = models.DecimalField(max_digits=10, decimal_places=2)
    freezed = models.DecimalField(max_digits=10, decimal_places=2)
    date_last_withdraw = models.DateTimeField()

    def has_balance(self,amount):
        return amount >= self.available
    
    def deposit(self, amount):
        self.available += amount
        self.save()
    
    def freeze(self, amount):
        self.freezed += amount
        self.save()
    
    def release(self, amount):
        if self.freezed >= amount:
            self.freezed -= amount
            self.deposit(amount)
    
    
# class Comment(models.Model):
#     product = models.ForeignKey(to=Product, related_name='comments', on_delete=models.CASCADE)
#     customer = models.ForeignKey(to=User, related_name='comments', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     published = models.BooleanField(default=False)
#     rate = models.PositiveBigIntegerField()
    
   
# class Favourite(models.Model):
#     product = models.ForeignKey(to=Product, related_name='likes', on_delete=models.CASCADE)
#     customer = models.ForeignKey(to=User, related_name='favourites', on_delete=models.CASCADE)
    