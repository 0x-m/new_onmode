# Generated by Django 4.0.3 on 2022-04-29 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0002_remove_coupon_reserved_discount_code_and_more'),
        ('orders', '0005_alter_order_address_alter_order_shop_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='promotions.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_fulfilled',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]