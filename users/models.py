
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
import secrets
import string
from decouple import config
from django.urls import reverse

class CustomUserManager(UserManager):
        
    def create_superuser(self, phone_num, email, password: str):
        u = self.model(phone_num=phone_num, email=self.normalize_email(email))
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)


class User(AbstractUser):
    MAX_STORAGE_SIZE = config('MAX_STORAGE', default=20, cast=int)
    #TODO:....
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
    use_custom_storage_capcity = models.BooleanField(default=False, help_text='check if you want arbitrary storage capacity for this user')
    custom_storage_capacity = models.FloatField(default=20, help_text='custom storage in mega bytes') #in MB
    consumed_storage = models.FloatField(default=0, help_text='consumed storage in mega bytes') #in MB
    



    @property 
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        return ' '
    
    
    @property
    def new_messages(self):
        return self.messages.filter(read=False).count()
    
    @property
    def cart_count(self):
        count = 0
        for order in self.orders.filter(paid=False).all():
            count += len(order)

        return count
    
  
    @property
    def has_completed_profile(self):
        return self.first_name and self.last_name
    
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
        return self.consumed_storage * 1024 * 1024
    
    def storage_has_capacity(self, size):
        '''
        size: in bytes
        '''
        max_capacity = self.MAX_STORAGE_SIZE
        if self.use_custom_storage_capcity:
            max_capacity = self.custom_storage_capacity

        return self.storage + size < max_capacity * 1024 * 1024
    
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
        
    @property
    def left_storage(self):
        #TODO: duplicate code.......
        max_capacity = self.MAX_STORAGE_SIZE
        if self.use_custom_storage_capcity:
            max_capacity = self.custom_storage_capacity

        return round(max_capacity - self.consumed_storage)

        


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
        to=User, related_name='wallet', on_delete=models.CASCADE)
    available = models.PositiveBigIntegerField(default=0)
    freezed = models.PositiveBigIntegerField(default=0)
    date_last_withdraw = models.DateTimeField(null=True, blank=True)

    def has_balance(self, amount):
        return amount <= self.available

    def deposit(self, amount):
        self.available += amount
        self.save()
        return True

    def withdraw(self, amount):
        if self.available >= amount:
            self.available -= amount
            self.date_last_withdraw = timezone.now()
            self.save()
            return True
        return False


    def update_date_last_withdraw(self):
        self.date_last_withdraw = timezone.now()
        self.save()

    @property
    def total(self):
        return self.available + self.freezed
    
    
    @property
    def last_checkout(self):
        return self.checkouts.order_by('date_created').last()
    
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
        return True

    def dec_freeze(self, amount):
        if self.freezed >= amount:
            self.freezed -= amount
            self.save()
            return True
        return False
    
    def release(self, amount):
        if self.freezed >= amount:
            self.freezed -= amount
            self.available += amount
            self.save()
            return True
        return False


    
class CheckoutRequest(models.Model):
    class STATES(models.TextChoices):
        InProgress = 'inp',
        Fulfilled = 'ful',
        Rejected = 'rej'

    wallet = models.ForeignKey(
        to=Wallet, on_delete=models.CASCADE, related_name='checkouts')
    merch_card = models.CharField(max_length=20, blank=True, null=True)
    amount = models.PositiveBigIntegerField(default=0)
    call_me = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=True)
    state = models.CharField(
        max_length=3, choices=STATES.choices, default=STATES.InProgress)

    date_created = models.DateTimeField(default=timezone.now)
    date_proceeded = models.DateTimeField(default=timezone.now)

    @property
    def fee(self):
        fee_percent = 0
        shop = self.wallet.user.shop
        if shop:
            fee_percent = shop.fee 
        return (fee_percent / 100) * self.amount
    
    @property
    def final_amount(self):
        return self.amount - self.fee
    
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
    amount = models.PositiveBigIntegerField(default=0)
    date_committed = models.DateTimeField(default=timezone.now)
    succeed = models.BooleanField(default=False)
    
    def apply(self):
        self.wallet.deposit(self.amount)
        self.date_committed = timezone.now()
        self.succeed = True
        self.save()
    


class TicketType(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title
    
class Ticket(models.Model):
    user = models.ForeignKey(to=User, related_name='tickets', on_delete=models.CASCADE)
    type = models.ForeignKey(to=TicketType, related_name='tickets', on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True)
    body = models.TextField(max_length=5000)
    seen_by_user = models.BooleanField(default=False)
    seen_by_intendant = models.BooleanField(default=False)
    can_reply = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('users:ticket', kwargs={'ticket_id': self.id})
    
    def __str__(self) -> str:
        return self.title + str(self.id)
    
    @property
    def no_unseens(self):
        if self.replies:
            return self.replies.filter(seen_by_user=False).count()
    
class TicketReply(models.Model):
    ticket = models.ForeignKey(to=Ticket, related_name='replies', on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)
    user = models.ForeignKey(to=User, 
                                 related_name='answered_tickets', 
                                 on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    seen_by_user = models.BooleanField(default=False)
    seen_by_intendant = models.BooleanField(default=False)
    


class Message(models.Model):
    class TYPES(models.TextChoices):
        NORMAL = 'Normal',
        WARNING = 'Warning',
        INFO = 'Info'
    user = models.ForeignKey(to=User, related_name='messages', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPES.choices, default=TYPES.INFO)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(max_length=5000, blank=True)
    read = models.BooleanField(default=False)
    
    