# Generated by Django 4.0.3 on 2022-05-25 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_orderitem_free_shipping_orderitem_shipping_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='shipping_cost',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]
