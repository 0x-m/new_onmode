from ast import arg
from django.db import models
from django.dispatch import receiver
from apps.catalogue.models import Shop
from django.db.models.signals import pre_delete
from django.utils.text import slugify
from tinymce.models import HTMLField
from onmode.storage_backends import SiteStorage


class SliderPhoto(models.Model):
    photo = models.ImageField(blank=True)
    photo_url = models.URLField(blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True)
    link = models.URLField(null=True, blank=True)
    precedence = models.PositiveIntegerField(default=0)


@receiver(pre_delete, sender=SliderPhoto)
def delet_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete()


class Certificate(models.Model):
    name = models.CharField(max_length=255, blank=True)
    symbol = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=1000)
    related_link = models.URLField(blank=True, null=True)
    show_on_index = models.BooleanField(default=False)


class About(models.Model):
    content = HTMLField()


class Law(models.Model):
    content = HTMLField()


class SiteInfo(models.Model):
    logo = models.ImageField(null=True, blank=True, storage=SiteStorage())
    favicon = models.ImageField(null=True, blank=True, storage=SiteStorage())
    site_title = models.CharField(max_length=255, blank=True)
    site_description = models.TextField(max_length=1000, blank=True)
    pinned_message = models.CharField(max_length=500, blank=True)
    pinned_color = models.CharField(max_length=10, blank=True)
    pinned_text_color = models.CharField(max_length=10, blank=True)
    pinned_url = models.URLField(null=True, blank=True)
    show_pinned_message = models.BooleanField(default=False)
    jumbo_message = models.TextField(max_length=1000, blank=True)
    jumbo_button_text = models.CharField(max_length=50, blank=True)
    jumbo_button_url = models.URLField(null=True, blank=True)
    show_jumbo_to = models.CharField(
        choices=[
            ("All", "All"),
            ("ShopKeeprs", "ShopKeepers"),
            ("Customers", "Customers"),
            ("GuestUser", "GeustUser"),
            ("NoOne", "NoOne"),
        ],
        max_length=20,
        default="All",
    )
    tel_line_1 = models.CharField(max_length=20, blank=True)
    tel_line_2 = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=1000, blank=True)
    email = models.EmailField(blank=True, null=True)
    blog = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    enable_GTM = models.BooleanField(default=False)
    GOOGLE_TAG_ID = models.CharField(max_length=255, blank=True)


class BlogPost(models.Model):
    photo = models.ImageField(null=True, storage=SiteStorage())
    photo_url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, null=True)


@receiver(pre_delete, sender=BlogPost)
def delet_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete()


class ShopSet(models.Model):
    shops = models.ManyToManyField(to=Shop)
    title = models.CharField(max_length=255, blank=True)
    slogan = models.CharField(max_length=255, blank=True)


class ContactUsType(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self) -> str:
        return self.title


class ContactUsMessage(models.Model):
    type = models.ForeignKey(
        to=ContactUsType, related_name="messages", on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(max_length=5000, blank=True)
    read = models.BooleanField(default=False)


class CreateShopGuide(models.Model):
    content = HTMLField()


class ReturnOrderGuide(models.Model):
    content = HTMLField()


class GeoLocation(models.Model):
    provinces = models.JSONField()
    cities = models.JSONField()

    def get_cities(self, province_id):
        _cities = []
        for city in self.cities:
            if str(city["province_id"]).strip() == str(province_id).strip():
                _cities.append(city["name"])
        return _cities


class SitePage(models.Model):
    en_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False)
    content = HTMLField()

    def save(self, *args, **kwargs):
        if self.en_name:
            self.slug = slugify(self.en_name)
        super().save(*args, **kwargs)
