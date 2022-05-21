# Generated by Django 4.0.3 on 2022-05-20 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_walletalternation_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='free_shipping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipping_cost',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]