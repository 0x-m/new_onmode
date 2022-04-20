
from email.policy import default
from itertools import product
from re import T
from statistics import mode
from django.db import models
from django.forms import modelformset_factory
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    slug = models.SlugField()
    en_slug = models.SlugField()
    meta_title = models.CharField(max_length=90)
    meta_keywords = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=100)
    parent = models.ForeignKey(to='self',
                               related_name='childs',
                               on_delete=models.CASCADE,
                               null=True)

    # photo = models.ForeignKey(to='Photo',
                            #   on_delete=models.DO_NOTHING,
                            #   null=True)

class Shop(models.Model):
    owner = models.ForeignKey(to='User', on_delete=models.SET_NULL)
    name = models.CharField(max_length=40)
    meta_title = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=400)
    #baner = models.ForeignKey(to='Photos', on_delete=models.SET_NULL)
    #logo = models.ForeignKey(to='Photo', on_delete=models.SET_NULL)
    address_description = models.TextField(max_length=1000)
    telephone = models.CharField(max_length=20)
    product_capacity = models.PositiveIntegerField(default=100)
    product_count = models.PositiveIntegerField(default=0)
    site_fee = models.PositiveIntegerField(default=9)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    supported_provinces = models.CharField(max_length=1000, blank=True, null=True)
    

class Attribute(models.Model):
    class ATTR_TYPES(models.TextChoices):
        Number = 'NUM', 'Number'
        Text = 'TXT', 'Text'
        Boolean = 'BOL', 'Boolean'
        Choices = 'CHO', 'Choices'
        MultiChoices = 'CHS', 'MultiChoices'
        Json = 'JSO', 'Json'

    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=3,
                            choices=ATTR_TYPES.choices,
                            default=ATTR_TYPES.Number)
    
    default = models.CharField(max_length=100, blank=True)
    choices = models.TextField(max_length=10000, blank=True)
    meta = models.JSONField(default={})
    description = models.CharField(max_length=400)
    
    


class Product(models.Model):
    shop = models.ForeignKey(to='shop', related_name='products')
    name = models.CharField(max_length=50, blank=False, null=False)
    en_name = models.CharField(max_length=50, blank=True, null=False)
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    en_slug = models.SlugField()
    meta_description = models.CharField(max_length=144)
    meta_keywords = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    upc = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0, blank=False)
    stock_low_threshold = models.IntegerField(default=1)
    free_shipping = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    sold_individually = models.BooleanField(default=False)
    tax = models.DecimalField()
    price = models.DecimalField(blank=False, null=False, default=0)
    has_sales = models.BooleanField(default=False)
    sales_price = models.DecimalField(blank=True, default=0)
    sales_from = models.DateTimeField(blank=True)
    sales_to = models.DateTimeField(blank=True)
    #discount = models....
    shipping_cost = models.DecimalField(blank=True)
    shipping_cost_description = models.TextField(max_length=1000)
    description = models.TextField(max_length=2000, blank=True)
    image = models.ImageField()
    # gallery = models.ForeignKey(to='gallery')
    more_attributes = models.JSONField(default={})
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(auto_now=True,
                                        null=True,
                                        editable=False)
    discount = models.ForeignKey(to='Discount',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    attributes = models.ManyToManyField(to=Attribute, related_name='products')
    attribute_values = models.JSONField(default={})
    
    

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
       


class Collection(models.Model):
    products = models.ManyToManyField(to=Product, related_name='collections')
    name = models.CharField(max_length=40)
    en_name = models.CharField(max_length=40)
    slug = models.SlugField()
    en_slug = models.SlugField()
    meta_title = models.CharField(max_length=40)
    meta_description = models.CharField(max_length=90)
    description = models.TextField(max_length=2000)
    photo = models.ForeignKey(to='Photo', on_delete=models.DO_NOTHING)
    #discount = models.ForeignKey(to='Discount', on_delete=models.SET_NULL, null=True, blank=True)
    prefer_collection_discount = models.BooleanField(default=False)
    
