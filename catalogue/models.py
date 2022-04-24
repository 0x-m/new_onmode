
from email.policy import default
import json
from operator import truediv
import string
from tokenize import String
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import pre_delete
import secrets
import string
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    en_slug = models.SlugField(blank=True)
    meta_title = models.CharField(max_length=90, blank=True)
    meta_keywords = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey(to='self',
                               related_name='childs',
                               on_delete=models.CASCADE,
                               null=True)

    # photo = models.ForeignKey(to='Photo',
                            #   on_delete=models.DO_NOTHING,
                            #   null=True)
    class Meta:
        verbose_name_plural = 'categories'


class Shop(models.Model):
    owner = models.ForeignKey(
        to=User, related_name='shops', on_delete=models.SET_NULL, null=True,)
    name = models.CharField(max_length=40)
    meta_title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=400)
    # baner = models.ForeignKey(to='Photos', on_delete=models.SET_NULL)
    # logo = models.ForeignKey(to='Photo', on_delete=models.SET_NULL)
    address_description = models.TextField(max_length=1000)
    phone = models.CharField(max_length=20)
    product_capacity = models.PositiveIntegerField(default=100)
    product_count = models.PositiveIntegerField(default=0)
    fee = models.PositiveIntegerField(default=9)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def has_capacity(self):
        return self.product_capacity > self.product_count

    @property
    def owner_phone(self):
        return self.owner.phone_num
    # NOTE: using signals for managing product counts..? bad idea!?

    def inc_product_count(self):
        if not self.has_capacity():
            return  # NOTE: raising Exception..??

        self.product_count += 1
        self.save()

    def dec_product_count(self):
        if not self.product_count > 0:
            return
        self.product_count -= 1
        self.save()

    def __str__(self) -> str:
        return self.meta_title


@receiver(pre_delete, sender=Shop)
def has_shop_hadler(sender, instance, **kwargs):
    instance.owner.has_shop = False
    instance.owner.save()


class Option(models.Model):
    class TYPES(models.TextChoices):
        Number = 'NUM', 'Number'
        Text = 'TXT', 'Text'
        Boolean = 'BOL', 'Boolean'
        Choices = 'CHO', 'Choices'
        MultiChoices = 'CHS', 'MultiChoices'
        Json = 'JSO', 'Json'

    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=3,
                            choices=TYPES.choices,
                            default=TYPES.Number)

    default = models.CharField(max_length=100, blank=True)
    choices = models.TextField(max_length=10000, blank=True)
    meta = models.JSONField(default=dict)
    description = models.CharField(max_length=400)

    def parse(self, value: str):
        try:
            if self.type == self.TYPES.Number:
                return int(value)
            elif self.type == self.TYPES.Text:
                return value
            elif self.type == self.TYPES.Boolean:
                return bool(value)
            elif self.type == self.TYPES.Choices or self.type == self.TYPES.MultiChoices:  # list of comma seperated
                temp = value.strip()
                items = temp.split(',')
                return items
            elif self.type == self.TYPES.Json:
                return json.loads(value)
        except Exception as e:
            pass  # TODO:

    @property
    def is_list(self):
        return self.type in [self.TYPES.Choices, self.TYPES.MultiChoices, self.TYPES.Json]


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    options = models.ManyToManyField(to=Option, related_name='types')


class CreateShopRequest(models.Model):
    user = models.ForeignKey(
        to=User, related_name='shop_requests', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, blank=False)
    name = models.CharField(max_length=20, blank=False)
    date_created = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    reject_status = models.TextField(max_length=1000, blank=True)

    def accept(self):
        shop = Shop(owner=self.user,
                    name=self.name,
                    meta_title=self.title, )

        self.user.make_me_shop(shop)
        self.accepted = True
        self.save()


class Product(models.Model):

    #TODO: variable code length
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(12))
        return code
        
        
    
    
    shop = models.ForeignKey(to=Shop, related_name='products', on_delete=models.CASCADE)
    prod_code = models.CharField(max_length=20, default=generate_code, editable=False)
    category = models.ForeignKey(to=Category, related_name='products', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(to=ProductType, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    en_name = models.CharField(max_length=50, blank=True, null=False)
    slug = models.SlugField(blank=True, null=True)
    en_slug = models.SlugField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField(default=0, blank=False)
    stock_low_threshold = models.IntegerField(default=1)
    free_shipping = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    sold_individually = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    has_sales = models.BooleanField(default=False)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # discount = models....
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(max_length=5000, blank=True)
    # image = models.ImageField()
    # gallery = models.ForeignKey(to='gallery')
    attributes = models.JSONField(default=dict)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(auto_now=True,
                                        null=True,
                                        editable=False)
    

    
    # discount = models.ForeignKey(to='Discount',
    #                              on_delete=models.SET_NULL,
    #                              null=True, blank=True)
    


    @property
    def is_available(self) -> bool:
        pass

    @property
    def has_valid_discount(self) -> bool:
        pass
    
    def inc_quantity(self, count=1):
        pass
    
    def dec_quantity(self, count=1):
        pass

    def get_price(self):
        pass
       


#TODO: stores similarity between products....
# class RelatedProduct(models.Model):
#     pass



class ProductStats(models.Model):
    product = models.OneToOneField(to=Product,
                                   on_delete=models.CASCADE,
                                   related_name='stats')
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    fails = models.IntegerField(default=0)
    rates_avg = models.FloatField(default=0)
    
    def inc_views(self):
        self.views += 1
        self.save()

    def dec_views(self):
        if (self.views > 0):
            self.views -= 1
            self.save()

    def inc_comments(self):
        self.comments += 1
        self.save()

    def dec_comments(self):
        if (self.comments > 0):
            self.comments -= 1
            self.save()

    def inc_likes(self):
        self.likes += 1
        self.save()

    def dec_likes(self):
        if (self.likes > 0):
            self.likes -= 1
            self.save()

    def inc_sales(self):
        self.sales += 1
        self.save()

    def dec_sales(self):
        if (self.sales > 0):
            self.sales -= 1
            self.save()
    
    def inc_fails(self):
        self.fails += 1
        self.save()
    
    def dec_fails(self):
        if (self.fails > 0):
            self.fails -= 1
            self.save()
    

# TODO: create a stats for shop


class Collection(models.Model):
    products = models.ManyToManyField(to=Product, related_name='collections')
    name = models.CharField(max_length=40)
    en_name = models.CharField(max_length=40)
    slug = models.SlugField()
    en_slug = models.SlugField()
    meta_title = models.CharField(max_length=40)
    meta_description = models.CharField(max_length=90)
    description = models.TextField(max_length=2000)
    # photo = models.ForeignKey(to='Photo', on_delete=models.DO_NOTHING)
    # discount = models.ForeignKey(to='Discount', on_delete=models.SET_NULL, null=True, blank=True)
    prefer_collection_discount = models.BooleanField(default=False)
    


class ProductOptionValue(models.Model):
    product = models.ForeignKey(to=Product, related_name='options', on_delete=models.CASCADE)
    option = models.ForeignKey(to=Option, related_name='option_values', on_delete=models.CASCADE)
    value = models.TextField(max_length=5000)
    