
import os
from django.db import models
from django.dispatch import receiver
from django.http import HttpRequest
from django.utils import timezone
from django.db.models.signals import pre_delete, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
import secrets
import string
from users.models import User
from promotions.models import Discount
from django.urls.base import reverse
import django_filters
from django.utils.text import slugify
from decouple import config
from onmode.storage_backends import SiteStorage


#TODO: move it to utils
def persian_slugify(txt: str):
    slug = ''
    for c in txt:
        if c not in [' ', ' ', '?', '(', ')', '%', '٪']:
            slug += c
        else:
            slug += '-'
    return slug

class Category(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, allow_unicode=True, null=True)
    en_slug = models.SlugField(blank=True, null=True)
    meta_title = models.CharField(max_length=90, blank=True)
    meta_keywords = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey(to='self',
                               related_name='childs',
                               on_delete=models.CASCADE,
                               null=True, blank=True)

    # photo = models.ForeignKey(to='Photo',
    #   on_delete=models.DO_NOTHING,
    #   null=True)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        name = self.name
        if self.parent:
            name = self.parent.name + '/' + self.name
        return name
    
    def save(self, *args, **kwargs):
        if self.en_name:
            self.en_slug = slugify(self.en_name)
        if self.name:
            self.slug = persian_slugify(self.name)
        super().save(*args, **kwargs)
        
            


class Shop(models.Model):
    MAX_PRODUCTS = config('SHOP_MAX_PRODUCT',default=100, cast=int)
    owner = models.ForeignKey(
        to=User, related_name='shops', on_delete=models.SET_NULL, null=True,)
    name = models.CharField(max_length=40)  # TODO: make it unique
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.CharField(max_length=400, blank=True)
    banner = models.ImageField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    address_description = models.TextField(max_length=1000, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    user_custom_product_capacity = models.BooleanField(default=False)
    product_capacity = models.PositiveIntegerField(default=100)
    product_count = models.PositiveIntegerField(default=0)
    fee = models.PositiveIntegerField(default=9)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def has_capacity(self):
        capacity = self.MAX_PRODUCTS
        if self.user_custom_product_capacity:
            capacity = self.product_capacity
        return capacity > self.product_count

    @property
    def owner_phone(self):
        return self.owner.phone_num
    # NOTE: using signals for managing product counts..? bad idea!?

    def inc_product_count(self):
        if not self.has_capacity():
            return Exception('max allowd product restriction')  # NOTE: raising Exception..??

        self.product_count += 1
        self.save()

    def dec_product_count(self):
        if not self.product_count > 0:
            return
        self.product_count -= 1
        self.save()

    def __str__(self) -> str:
        return self.name


@receiver(post_save, sender=Shop)
def set_has_shop(sender, instance, created, **kwawrgs):
    if created:
        instance.owner.has_shop = True

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
    
    fa_name = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=3,
                            choices=TYPES.choices,
                            default=TYPES.Number)

    default = models.CharField(max_length=100, blank=True)
    identifier = models.CharField(max_length=255, blank=True)
    choices = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.name

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

    # TODO: variable code length
    def generate_code():
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(12))
        return code

    shop = models.ForeignKey(
        to=Shop, related_name='products', on_delete=models.CASCADE)
    prod_code = models.CharField(
        max_length=20, default=generate_code, editable=False)
    category = models.ForeignKey(
        to=Category, related_name='products', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=False, null=False, db_index=True)
    en_name = models.CharField(max_length=50, blank=True, null=False, db_index=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    en_slug = models.SlugField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True, db_index=True)
    meta_description = models.CharField(max_length=255, blank=True, db_index=True)
    meta_keywords = models.CharField(max_length=255, blank=True, db_index=True)
    sku = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField(default=0, blank=False)
    stock_low_threshold = models.IntegerField(default=1)
    free_shipping = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    sold_individually = models.BooleanField(default=False)
    price = models.PositiveBigIntegerField(default=0)
    has_sales = models.BooleanField(default=False)
    sales_price = models.PositiveBigIntegerField(default=0)
    shipping_cost = models.PositiveBigIntegerField(default=0)
    description = models.TextField(max_length=5000, blank=True)
    attributes = models.JSONField(default=dict, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(auto_now=True,
                                        null=True,
                                        editable=False)
    preview = models.ForeignKey(
        to='Photo', related_name='preview', on_delete=models.SET_NULL, null=True)
    discount = models.ForeignKey(to=Discount,
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    relateds = models.ManyToManyField(to='self')



    def save(self, *args, **kwargs):
        if self.en_name:
            self.en_slug = slugify(self.en_name)
        if self.name:
            self.slug = persian_slugify(self.name)
        super().save(*args, **kwargs)



    @property
    def colors(self):
        try:
            colors = Option.objects.get(name='color').choices
            product_colors = self.options.get(
                option__name='color').value.split(',')
            res = []
            for color in colors:
                if str(color['id']) in product_colors:
                    res.append(color)
            return res
        except:
            pass


    @property
    def sizes(self):
        try:
            sizes = Option.objects.get(name='size').choices
            product_colors = self.options.get(option__name='size').value.split(',')
            res = []
            for size in sizes:
                if str(size['id']) in product_colors:
                    res.append(size)
            
            return res
        except:
            pass       
    
    
    @property
    def get_shipping_cost(self):
        if self.free_shipping:
            return 0
        else:
            self.shipping_cost

    @property
    def is_available(self) -> bool:
        pass

    def inc_quantity(self, count=1):
        pass

    def dec_quantity(self, count=1):
        if self.has_quantity(count):
            self.quantity -= count
        self.save()
    
    def force_dec_quantity(self, count):
        c = self.quantity - count
        if c < 0:
            c = 0
        self.quantity = c
        self.save()    
        
    def has_quantity(self, q):
        return self.quantity >= q

    def get_discount(self, collection=None):
        discount = self.discount
        if collection and collection.discount:
            if self in collection.products.all():
                if collection.prefer_collection_discount or not discount:
                    discount = collection.discount
        return discount



    def compute_price(self, collection=None):

        discount = self.get_discount(collection)

        price = self.price
        if self.has_sales:
            price = self.sales_price

        if discount:
            if discount.is_valid():
                difference = round(price * (discount.percent / 100))
                if difference <= discount.max_amount:
                    price -= difference
                else:
                    price -= discount.max_amount
        if price < 0:
            price = 0

        return price

    def __str__(self) -> str:
        return self.name + f'({self.id})'

def get_brand(request: HttpRequest):
    if request is None:
        return Product.objects.none()
    
    brand_ids = request.GET.getlist('brands')
    print(brand_ids)
    products = Product.objects.filter(options__option__name='brand', options__value__in=brand_ids).all()

    print(products)
    return products



class ProductFilter(django_filters.FilterSet):
    categories = django_filters.BaseInFilter(field_name='category__id')
    brands = django_filters.CharFilter(method='brand_filter')
    colors = django_filters.CharFilter(method='color_filter')
    sizes = django_filters.CharFilter(method='filter_size')
    has_sales = django_filters.BooleanFilter(field_name='has_sales')
    orderby = django_filters.CharFilter(method='order_by')
    def brand_filter(self, queryset, name, value):
        ls = self.request.GET.getlist('brands')
        return queryset.filter(options__option__name='brand', options__value__in=ls)
    
    
    def color_filter(self, queryset, name, value):
        ids = self.request.GET.getlist('colors')
       
        # TODO: below code repeat two times....
        rx = '('
        for i in ids:
            rx += (i +',|')
        rx = rx[:len(rx) - 1]
        rx += ')'
       
        return queryset.filter(options__option__name='color', options__value__regex=rx)
    
    
    def size_filter(self, queryset, name, value):
        ids = self.request.GET.getlist('sizes')
        rx = '('
        for i in ids:
            rx += (i + ',|')
        rx = rx[:len(rx) -1]
        rx += ')'
        
        return queryset.filter(options__option__name='size', options__option__regex=rx)
        
    
    def order_by(self, queryset, name, value):
        if value == 'newest':
            return queryset.order_by('-date_created')
        elif value == 'popular':
            return queryset.order_by('-stats__likes')
        elif value == 'bestselling':
            return queryset.order_by('-stats__sales')
        elif value == 'hot':
            return queryset.order_by('-stats__comments')
            
        return queryset

        
        
    
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'lt'],
        }





class ProductStats(models.Model):
    product = models.OneToOneField(to=Product,
                                   on_delete=models.CASCADE,
                                   related_name='stats')
    views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    comments = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    # sales = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    # fails = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rates_avg = models.FloatField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(5)
    ])

    @property
    def rate(self):
        return range(int(self.rates_avg))

    @property
    def rate_complement(self):
        return range(5 - len(self.rate))
        

    @property
    def number_of_sells(self):
        return self.product.orders.filter(order__state='fulfilled').count()
    
    def inc_views(self):
        self.views += 1
        self.save()

    def dec_views(self):
        if (self.views > 0):
            self.views -= 1
            self.save()

    def inc_comments(self, rate):
        new_rate_avg = (self.comments * self.rates_avg + rate) / (self.comments + 1)
        self.comments += 1
        self.rates_avg = new_rate_avg
        self.save()

    def dec_comments(self, rate):
        if (self.comments > 0):
            new_rate_avg = (self.comments * self.rates_avg - rate) / (self.comments - 1)
            self.comments -= 1
            self.rates_avg = new_rate_avg
            self.save()

    def inc_likes(self):
        self.likes += 1
        self.save()

    def dec_likes(self):
        if (self.likes > 0):
            self.likes -= 1
            self.save()

    # def inc_sales(self):
    #     self.sales += 1
    #     self.save()

    # def dec_sales(self):
    #     if (self.sales > 0):
    #         self.sales -= 1
    #         self.save()

    # def inc_fails(self):
    #     self.fails += 1
    #     self.save()

    # def dec_fails(self):
    #     if (self.fails > 0):
    #         self.fails -= 1
    #         self.save()
    
    


@receiver(post_save, sender=Product)
def create_stats(sender, instance, created, **kwargs):
    if created:
        ProductStats.objects.get_or_create(product=instance)



# TODO: create a stats for shop


class Collection(models.Model):
    products = models.ManyToManyField(to=Product, related_name='collections')
    featureds = models.CharField(max_length=1000, blank=True)
    name = models.CharField(max_length=40, unique=True)
    en_name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(editable=False, blank=True, null=True, allow_unicode=True)
    en_slug = models.SlugField(editable=False, blank=True, null=True)
    slogan = models.CharField(max_length=1000, blank=True)
    meta_title = models.CharField(max_length=40, blank=True)
    meta_description = models.CharField(max_length=90, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    discount = models.ForeignKey(
        to=Discount, on_delete=models.SET_NULL, null=True, blank=True)
    prefer_collection_discount = models.BooleanField(default=False)
    page_poster_alt = models.CharField(max_length=255, blank=True)
    page_poster_url = models.URLField(blank=True, null=True)
    page_poster = models.ImageField(null=True, blank=True, storage=SiteStorage())
    index_view = models.BooleanField(default=False)
    index_poster = models.ImageField(null=True, blank=True, storage=SiteStorage())
    index_poster_url = models.URLField(null=True, blank=True)
    index_poster_link = models.URLField(blank=True, null=True)
    index_poster_alt = models.CharField(max_length=255, blank=True)

    @property
    def get_featureds(self):
        featureds = None
        if self.featureds:
            ids = self.featureds.split(',')
            featureds = self.products.filter(id__in=ids)
        return featureds
    
    def get_absolute_url(self):
        return reverse('catalogue:collection', kwargs={'collection_name':self.en_name})
    
    def save(self, *args, **kwargs):
        if self.en_name:
            self.en_slug = slugify(self.en_name)
        if self.name:
            self.slug = persian_slugify(self.name)
        super().save(*args, **kwargs)
        


    

class ProductOptionValue(models.Model):
    product = models.ForeignKey(
        to=Product, related_name='options', on_delete=models.CASCADE)
    option = models.ForeignKey(
        to=Option, related_name='option_values', on_delete=models.CASCADE)
    value = models.TextField(max_length=5000)
    


class Photo(models.Model):

    def generate_path(instance, filename):
        return os.path.join('product', str(instance.product.id), 'photos', filename)

    product = models.ForeignKey(
        to=Product, related_name='photos', on_delete=models.CASCADE)
    img = models.ImageField(upload_to=generate_path)
    url = models.URLField(null=True)
    alt = models.CharField(max_length=255, blank=True)


class Comment(models.Model):
    product = models.ForeignKey(to=Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    published = models.BooleanField(default=False)
    rate = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    
    @property
    def prod_rate(self):
        return range(self.rate)
    
    @property
    def prod_rate_complement(self):
        return range(5 - self.rate)
    
    

@receiver(post_save, sender=Comment)
def increase_comments(sender, instance: Comment, created, **kwargs):
    if created:
        instance.product.stats.inc_comments(instance.rate)

@receiver(pre_delete, sender=Comment)
def decrease_comment(sender, instance, **kwargs):
    instance.product.stats.dec_comments(instance.rate)
    
    
   
class Favourite(models.Model):
    product = models.ForeignKey(to=Product, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='favourites', on_delete=models.CASCADE)

@receiver(post_save, sender=Favourite)
def increase_comments(sender, instance: Comment, created, **kwargs):
    if created:
        instance.product.stats.inc_likes()

@receiver(pre_delete, sender=Favourite)
def decrease_comment(sender, instance, **kwargs):
    instance.product.stats.dec_likes()
    
    