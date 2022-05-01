# Generated by Django 4.0.3 on 2022-05-01 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import promotions.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotions', '0002_remove_coupon_reserved_discount_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcard',
            name='code',
            field=models.CharField(default=promotions.models.GiftCard.generate_code, editable=False, max_length=15),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gifts', to=settings.AUTH_USER_MODEL),
        ),
    ]
