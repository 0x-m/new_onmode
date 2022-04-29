# Generated by Django 4.0.3 on 2022-04-29 05:43

from django.db import migrations, models
import promotions.models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='reserved',
        ),
        migrations.AddField(
            model_name='discount',
            name='code',
            field=models.CharField(default=promotions.models.Discount.generate_code, editable=False, max_length=8),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='max_amount',
            field=models.PositiveBigIntegerField(default=10000),
        ),
    ]
