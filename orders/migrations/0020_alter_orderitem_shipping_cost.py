# Generated by Django 4.0.3 on 2022-05-25 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_alter_orderitem_shipping_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='shipping_cost',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]