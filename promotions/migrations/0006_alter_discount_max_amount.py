# Generated by Django 4.0.3 on 2022-05-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0005_alter_giftcard_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='max_amount',
            field=models.PositiveBigIntegerField(default=10000),
        ),
    ]