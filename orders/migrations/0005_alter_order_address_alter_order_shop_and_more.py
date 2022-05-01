# Generated by Django 4.0.3 on 2022-04-29 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_consumed_storage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0034_alter_product_price_alter_product_sales_price_and_more'),
        ('orders', '0004_alter_order_code_alter_order_coupon_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='catalogue.shop'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]