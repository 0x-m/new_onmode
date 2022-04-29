from turtle import title
from django.db import models
from django.dispatch import receiver

from catalogue.models import  Shop
from django_quill.fields import QuillField
from django.db.models.signals import pre_delete


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


class About(models.Model):
    content = QuillField()


class Law(models.Model):
    content = QuillField()


class SiteInfo(models.Model):
    logo = models.ImageField(null=True, blank=True)
    favicon = models.ImageField(null=True, blank=True)
    site_title = models.CharField(max_length=255, blank=True)
    site_description = models.TextField(max_length=1000, blank=True)
    pinned_message = models.CharField(max_length=500, blank=True)
    pinned_color = models.CharField(max_length=10, blank=True)
    pinned_text_color = models.CharField(max_length=10, blank=True)
    pinned_url = models.URLField(null=True, blank=True)
    jumbo_message = models.TextField(max_length=1000, blank=True)
    jumbo_button_text = models.CharField(max_length=50, blank=True)
    jumb_button_url = models.URLField(null=True, blank=True)

    tel_line_1 = models.CharField(max_length=20, blank=True)
    tel_line_2 = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=1000, blank=True)
    email = models.EmailField(blank=True, null=True)

    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)


class BlogPost(models.Model):
    photo = models.ImageField(null=True)
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

