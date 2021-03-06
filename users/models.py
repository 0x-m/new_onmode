
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
import secrets
import string


# from catalogue.models import Product


class CustomUserManager(UserManager):
        
    def create_superuser(self, phone_num, email, password: str):
        u = self.model(phone_num=phone_num, email=self.normalize_email(email))
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        w = Wallet.objects.create(user=u)
        w.save()


class User(AbstractUser):
    MAX_STORAGE_SIZE = 20 * 1024  * 1024 #move to env
    def generate_usecode():
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(8))
        return code
    
    username = None

    email = models.EmailField()
    phone_num = models.CharField(max_length=11,
                                 validators=[
                                    RegexValidator('^09[0-9]{9}$')
                                     ], unique=True)
    gender = models.CharField(max_length=10, choices=[(
        'man', 'man'), ('woman', 'woman')], blank=True)
    user_code = models.CharField(max_length=20, default=generate_usecode, editable=False)
    referral_code = models.CharField(max_length=20, blank=True, null=True)
    request_for_shop = models.BooleanField(default=False)
    request_accepted = models.BooleanField(default=False)
    has_shop = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_num'

    objects = CustomUserManager()
    has_password = models.BooleanField(default=False)
    consumed_storage = models.FloatField(default=0) #in MB



    @property
    def paid_orders(self):
        return self.orders.filter(paid=True).all()

    @property
    def shop(self):
        shop = None
        if self.has_shop:
            shop = self.shops.first()
        return shop

    def make_me_shop(self, shop):
        '''
        first checks if current user has any shop
        if so, do nothing, othewise make a shop for the user
        '''
        if self.has_shop:
            return
        shop.owner = self
        shop.save()
        
        self.has_shop = True
        self.save()
    
    @property
    def storage(self):
        '''
        Get user consumed storage size in bytes
        '''
        return self.consumed_storage * 1024 *1024
    
    def storage_has_capacity(self, size):
        '''
        size: in bytes
        '''
        return self.storage + size < self.MAX_STORAGE_SIZE
    
    def consume_storage(self, size):
        '''
        size in bytes
        '''
        size_mb = size / (1024*1024)
        self.consumed_storage += size_mb #TODO:
        self.save()
    
    def free_storage(self, size):
        '''
        size in bytes
        '''
        size_mb = size / (1024*1024)
        self.consumed_storage -= size_mb
        self.save()


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.get_or_create(user=instance)


class Address(models.Model):
    user = models.ForeignKey(
        to=User, related_name='addresses', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    postal_code = models.CharField(max_length=20)
    removed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.full_name) + '/' + str(self.province) + '/' + str(self.city) + '/' + str(self.town)


class Wallet(models.Model):
    user = models.OneToOneField(
        to=User, related_name='wallet', on_delete=models.CASCADE, primary_key=True)
    available = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    freezed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_last_withdraw = models.DateTimeField(null=True, blank=True)

    def has_balance(self, amount):
        return amount >= self.available

    def deposit(self, amount):
        self.available += amount
        self.save()

    def withdraw(self, amount):
        if self.available >= amount:
            self.available -= amount
            self.date_last_withdraw = timezone.now()
            self.save()


    def update_date_last_withdraw(self):
        self.date_last_withdraw = timezone.now()
        self.save()

    @property
    def total(self):
        return self.available + self.freezed
    
    @property
    def allow_withdraw(self):
        
        t = timezone.now()
        
        # TODO: move period to the env file
        period = 6
        
        if not self.date_last_withdraw:
            return True

        return t >= self.date_last_withdraw + timezone.timedelta(days=period)



    
    
    def inc_freeze(self, amount):
        self.freezed += amount
        self.save()

    def dec_freeze(self, amount):
        if self.freezed >= amount:
            self.freezed -= amount
            self.save()
    
    def release(self, amount):
        if self.freezed >= amount:
            self.freezed -= amount
            self.available += amount
            self.save()
            


    
class CheckoutRequest(models.Model):

    class STATES(models.TextChoices):
        InProgress = 'inp',
        Fulfilled = 'ful',
        Rejected = 'rej'

    wallet = models.ForeignKey(
        to=Wallet, on_delete=models.CASCADE, related_name='checkouts')
    merch_card = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    call_me = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=True)
    state = models.CharField(
        max_length=3, choices=STATES.choices, default=STATES.InProgress)

    date_created = models.DateTimeField(default=timezone.now)
    date_proceeded = models.DateTimeField(default=timezone.now)

    def fulfill(self):
        self.wallet.withdraw(self.amount)
        self.date_proceeded = timezone.now()
        self.state = self.STATES.Fulfilled
        self.save()

    def save(self, *args, **kwargs):
        self.wallet.update_date_last_withdraw();
        super().save(*args, **kwargs)

        
    def reject(self):
        self.date_proceeded = timezone.now()
        self.state = self.STATES.Rejected
        self.save()

    def __str__(self) -> str:
        return 'Checkout request Number:  ' + str(self.id)

    
class DepositTransaction(models.Model):
    wallet = models.ForeignKey(to=Wallet, related_name='deposits', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_committed = models.DateTimeField(default=timezone.now)
    succeeded = models.BooleanField(default=False)
    
    def apply(self):
        self.wallet.deposit(self.amount)
        self.date_committed = timezone.now()
        self.succeeded = True
        self.save()
    
    
