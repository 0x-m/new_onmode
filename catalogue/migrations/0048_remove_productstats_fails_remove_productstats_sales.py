# Generated by Django 4.0.3 on 2022-05-08 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0047_shop_user_custom_product_capacity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productstats',
            name='fails',
        ),
        migrations.RemoveField(
            model_name='productstats',
            name='sales',
        ),
    ]
